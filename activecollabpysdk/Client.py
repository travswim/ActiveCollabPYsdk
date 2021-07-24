from io import BufferedReader
from typing import Any
from Exceptions import InvalidArgumentError
from Token import Token
import validators 
from urllib import parse
import requests
import os

class Client:
    """Client connection class for connecting to ActiveCollab API"""

    def __init__(self, token: Token, api_version: int = None) -> None:
        self.__token = token
        
        if api_version != None:
            if type(api_version) == int and api_version > 0:
                self.__api_version = api_version
            else:
                raise InvalidArgumentError("Not a valid API version")

        self.__header = {'X-Angie-AuthApiToken: ' + self.token}
    
    # Getter & Setter properties
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


    def __prepare_url(self, url: str) -> str:
        """Prepares a given URL for making http requests"""
        if not url:
            raise InvalidArgumentError("Invalid URL")

        parse_url = parse(url)
            
        path = parse_url.path or '/'
        
        path = '/' + path if path[0] == '/' else path

        query = '/' + parse_url.query if parse_url.query else ''

        return self.url + 'api/v' + self.api_version + path + query

    def __prepare_params(self, params: dict) -> dict:
        """Prepare given dictionary {parameters} to post to ActiveCollab"""
        return params or {}

    def __prepare_files(self, attachments: list[str]) -> dict[str, BufferedReader]:
        """Converts a list file paths to post to ActiveCollab"""

        file_params = {}

        if attachments:
            counter = 1

            for attachment in attachments:
                path = attachment[0] if type(attachment) is list else attachment

                if not os.path.isfile(path):
                    raise FileNotFoundError(f'{path} not found')

                with open(path, 'rb') as file:
                    file_params['attachment_' + str(counter)] = file
                    counter +=1

        return file_params

        
    def get(self, url: str) -> str:
        """HTTP Get request from ActiveCollab"""
        try:
            r = requests.get(url=self.__prepare_url(url), headers=self.__header)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return r.json()

    def post(self, url: str, params: dict = {}, attachments: list[str] = []) -> None:
        """HTTP Post request to ActiveCollab"""
        try:

            r = requests.post(url=self.__prepare_url(url), json=self.__prepare_params(params), headers=self.__header, files=self.__prepare_files(attachments))
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
                raise SystemExit(e)

    def delete(self, url:str, params: dict):
        """HTTP Delete request to ActiveCollab"""
        try:
            r = requests.delete(url = self.__prepare_url(url), headers=self.__header, json=self.__prepare_params(params))
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
                raise SystemExit(e)