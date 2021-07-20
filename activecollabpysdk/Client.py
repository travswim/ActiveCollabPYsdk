from typing import Any
from Exceptions import InvalidArgumentError
from Token import Token
import validators 
from urllib import parse
import requests
class Client:

    def __init__(self, token: Token, api_version: int = None) -> None:
        self.__token = token
        
        if api_version != None:
            if type(api_version) == int and api_version > 0:
                self.__api_version = api_version
            else:
                raise InvalidArgumentError("No a valid API version")
    @property
    def token(self):
        return self.__token.token

    @token.setter
    def token(self, value: str):
        if value != None:
            self.__token.token = value
        else:
            raise ValueError("Cannot be None")

    @property
    def url(self):
        return self.__token.url

    @url.setter
    def url(self, value: str):
        if validators.url(Any(value)) and value:
            self.__url = value
        else:
            raise InvalidArgumentError("URL is not valid")

    @property
    def api_version(self):
        return self.__api_version

    @api_version.setter
    def api_version(self, value: int):
        if value > 0:
            self.__api_version = value
        else:
            raise InvalidArgumentError("Invalid API version")

    def __prepare_header(self):
        return ['X-Angie-AuthApiToken: ' + self.token]

    def __prepare_url(self, url: str) -> str:
        if not url:
            raise InvalidArgumentError("Invalid URL")

        parse_url = parse(url)
            
        path = parse_url.path or '/'
        
        path = '/' + path if path[0] == '/' else path

        query = '/' + parse_url.query if parse_url.query else ''

        return self.url + 'api/v' + self.api_version + path + query

    def __prepare_params(self, params: dict):
        return params or {}

    def __prepare_files(self, file_paths: list[str]):
        files = {}
        for file in file_paths:
            try:


        
    def get(self, url: str) -> str:
        try:
            r = requests.get(url=self.__prepare_url(url), headers=self.__prepare_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return r.json()

    def post(self, url: str, params: dict = {}):
        try:
            r = requests.post(url=self.__prepare_url(url), json=self.__prepare_params(params), headers=self.__prepare_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
                raise SystemExit(e)

    