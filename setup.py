from pkg_resources import parse_requirements
from setuptools import setup, find_packages
import pathlib

__package_dir__ = 'src'

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in parse_requirements(requirements_txt)
    ]

setup(
    version='0.0.1',
    name='client_external_stubber_python',
    description='A client for the external stubber',
    url='https://github.com/navetas-loop/client-external-stubber-python',
    packages=find_packages(__package_dir__),
    package_dir={'': __package_dir__},
    install_requires=install_requires
)
