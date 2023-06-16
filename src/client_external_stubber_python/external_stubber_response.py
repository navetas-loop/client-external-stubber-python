from typing import Optional, Any, Mapping

from responses import Response, matchers


class ExternalStubberQueryParametersMatcher:
    def __init__(
            self,
            params: Mapping[str, str],
            strict_match: bool = True
    ):
        self.params = params
        self.strict_match = strict_match

    def to_dict(self):
        return {
            'params': self.params,
            'strict_match': self.strict_match
        }

    @classmethod
    def from_dict(cls, dictionary_representation):
        if dictionary_representation is None:
            return None

        return ExternalStubberQueryParametersMatcher(
            dictionary_representation['params'],
            dictionary_representation['strict_match']
        )


class ExternalStubberHeadersMatcher:
    def __init__(
            self,
            headers: Mapping[str, str],
            # defaulting to non-strict match here, as API Gateway adds *many* headers
            strict_match: bool = False
    ):
        self.headers = headers
        self.strict_match = strict_match

    def to_dict(self):
        return {
            'headers': self.headers,
            'strict_match': self.strict_match
        }

    @classmethod
    def from_dict(cls, dictionary_representation):
        if dictionary_representation is None:
            return None

        return ExternalStubberHeadersMatcher(
            dictionary_representation['headers'],
            dictionary_representation['strict_match']
        )


class ExternalStubberResponse:
    def __init__(
            self,
            method: str,
            path: str,
            params: ExternalStubberQueryParametersMatcher = None,
            body: str = None,
            json: Optional[Any] = None,
            status: int = 200,
            headers: ExternalStubberHeadersMatcher = None
    ):
        self.method = method
        self.path = path
        self.status = status
        self.headers = headers
        self.params = params
        self.body = body
        self.json = json

        if json:
            assert not body; 'Can\'t specify both `body` and `json`'

    def to_dict(self):
        params_dict = self.params.to_dict() if self.params else None
        headers_dict = self.headers.to_dict() if self.headers else None

        return {
            'method': self.method,
            'path': self.path,
            'params': params_dict,
            'headers': headers_dict,
            'body': self.body,
            'json': self.json,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, dictionary_representation):
        external_stubber_query_parameters_matcher = ExternalStubberQueryParametersMatcher.from_dict(dictionary_representation['params']) if 'params' in dictionary_representation else None
        external_stubber_headers_matcher = ExternalStubberHeadersMatcher.from_dict(dictionary_representation['headers']) if 'headers' in dictionary_representation else None

        return ExternalStubberResponse(
            dictionary_representation['method'],
            dictionary_representation['path'],
            external_stubber_query_parameters_matcher,
            dictionary_representation['body'],
            dictionary_representation['json'],
            dictionary_representation['status'],
            external_stubber_headers_matcher
        )

    def to_response(self) -> Response:
        matchers_list = []

        if self.params:
            matchers_list.append(
                matchers.query_param_matcher(
                    self.params.params,
                    strict_match=self.params.strict_match
                )
            )

        if self.headers:
            matchers_list.append(
                matchers.header_matcher(
                    self.headers.headers,
                    strict_match=self.headers.strict_match
                )
            )

        return Response(
            self.method,
            self.path,
            self.body,
            self.json,
            self.status,
            match=matchers_list,
        )
