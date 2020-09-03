import requests


class ApiClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def call(self, title: str = '', body: str = ''):
        requests.post(f'{self.host}:{self.port}/record', json={'title': title, 'body': body})
