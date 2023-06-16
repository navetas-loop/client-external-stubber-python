import json

import requests

from client_external_stubber_python.external_stubber_response import ExternalStubberResponse


class StubberClient:
    def __init__(self, base_url, error_on_unconsumed_requests=True, timeout_minutes=5):
        self.base_url = base_url
        self.timeout_minutes = timeout_minutes
        self.error_on_unconsumed_requests = error_on_unconsumed_requests

        self.session_id = None

    def __enter__(self):
        self.session_id = self.create_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unconsumed_responses = self.delete_session()

        if self.error_on_unconsumed_requests and unconsumed_responses != 0:
            raise Exception(f'Stubbing session finished with {unconsumed_responses} unconsumed responses')

    def create_session(self):
        response = requests.post(
            self.base_url + '/session',
            params={
                'timeout_minutes': self.timeout_minutes
            }
        )

        response.raise_for_status()

        session_id = response.json()['session_id']

        print(f'Started stubbing session {session_id}')

        return session_id

    def delete_session(self):
        response = requests.delete(
            self.base_url + f'/session/{self.session_id}'
        )

        response.raise_for_status()

        return response.json()['unconsumed_responses']

    def add_responses(self, responses: [ExternalStubberResponse]):
        response = requests.post(
            self.base_url + f'/session/{self.session_id}/responses',
            json={
                'responses': [json.dumps(response.to_dict()) for response in responses]
            }
        )

        response.raise_for_status()
