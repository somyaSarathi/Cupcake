import os
import json
import requests
from dotenv import load_dotenv

# load env file data
load_dotenv()
CLIENT: dict = {
    'ID': os.getenv('JDOODLEID'),
    'SECRET': os.getenv('JDOODLES')
}


class Compiler:
    def __init__(self, code: str, lang: str='py') -> None:
        self.lang = lang
        self.code = code

    def run(self) -> dict:
        output = None

        if self.lang == 'py' or self.lang == 'python':
            output = python3(self.code)

        if self.lang == 'js':
            output = nodejs(self.code)

        if self.lang == 'java':
            output = java(self.code)

        if self.lang == 'cpp' or self.lang == 'cc' or self.lang == 'c++':
            output = cplusplus(self.code)

        if self.lang == 'c':
            output = c(self.code)

        return output
    


def python3(code: str):
    '''
    - executes python3 program
    - returns output as a dict
    '''
    post_url = 'https://api.jdoodle.com/v1/execute'

    return (json.loads(requests.post(
        post_url,
        json={
            "script": code,
            "language": "python3",
            "versionIndex": "4",
            "clientId": CLIENT['ID'],
            "clientSecret": CLIENT['SECRET']
        }
    ).content))


# def python2(code: str):
#     '''
#     - executes python2 program
#     - returns output as a dict
#     '''
#     post_url = 'https://api.jdoodle.com/v1/execute'

#     return (json.loads(requests.post(
#         post_url,
#         json={
#             "script": code,
#             "language": "python2",
#             "versionIndex": "3",
#             "clientId": CLIENT['ID'],
#             "clientSecret": CLIENT['SECRET']
#         }
#     ).content))


def cplusplus(code: str):
    '''
    - executes c++ program
    - returns output as a dict
    '''
    post_url = 'https://api.jdoodle.com/v1/execute'

    return (json.loads(requests.post(
        post_url,
        json={
            "script": code,
            "language": "cpp17",
            "versionIndex": "1",
            "clientId": CLIENT['ID'],
            "clientSecret": CLIENT['SECRET']
        }
    ).content))


def c(code: str):
    '''
    - executes c program
    - returns output as a dict
    '''
    post_url = 'https://api.jdoodle.com/v1/execute'

    return (json.loads(requests.post(
        post_url,
        json={
            "script": code,
            "language": "c",
            "versionIndex": "4",
            "clientId": CLIENT['ID'],
            "clientSecret": CLIENT['SECRET']
        }
    ).content))


def nodejs(code: str):
    '''
    - executes nodejs program
    - returns output as a dict
    '''
    post_url = 'https://api.jdoodle.com/v1/execute'

    return (json.loads(requests.post(
        post_url,
        json={
            "script": code,
            "language": "nodejs",
            "versionIndex": "4",
            "clientId": CLIENT['ID'],
            "clientSecret": CLIENT['SECRET']
        }
    ).content))


def java(code: str):
    '''
    - executes java program
    - returns output as a dict
    '''
    post_url = 'https://api.jdoodle.com/v1/execute'

    return (json.loads(requests.post(
        post_url,
        json={
            "script": code,
            "language": "java",
            "versionIndex": "4",
            "clientId": CLIENT['ID'],
            "clientSecret": CLIENT['SECRET']
        }
    ).content))
