from io import BufferedReader
from typing import Any

from requests.models import Response
from activecollabpysdk.Exceptions import InvalidArgumentError
from activecollabpysdk.token_sdk import Token
from urllib import parse
import requests
import os
from activecollabpysdk.client_interface import ClientInterface

class Client(ClientInterface):
    """Client connection class for connecting to ActiveCollab API"""
    
    def __init__(self, token: Token, api_version: int = 1) -> None:
        self.token = token

        if api_version < 0:
            raise InvalidArgumentError(f'{api_version} is not a valid API version')
        self.api_version = api_version
        self.header = {"X-Angie-AuthApiToken" : self.token.token}
        self.info_response: Any = False
    
    

    def _prepare_url(self, url: str) -> str:
        """Prepares a given URL for making http requests

        Formats a url and checks if it is valid. Used by post, get, put, and delete requests to ActiveCollab

        :param str url: Requests URL
        :return: A valid URL
        :rtype: str
        """
        if not url:
            raise InvalidArgumentError(f'{url} is invalid')

        parse_url = parse.urlsplit(url)

        path = parse_url.path or '/'

        # path = '/' + path if path[0] != '/' else path
        path = f'/{path}' if path[0] != '/' else path


        # query = '/' + parse_url.query if parse_url.query else ''
        query = f'/{parse_url.query}' if parse_url.query else ''

        # return self.token.url + '/api/v' + str(self.api_version) + path + query
        return f'{self.token.url}/api/v{str(self.api_version)}{path}{query}'


    # def __prepare_params(self, params: dict[str, Any]) -> dict[str, Any]:
    #     """Prepare given dictionary {parameters} to post to ActiveCollab
        
    #     :param dict[str, Any] params: Paramerters to pass as data or JSON to ActiveCollab
    #     :return: A dictionary of 
    #     """
    #     return params or {}

    def _prepare_files(self, attachments: list[str] | None) -> dict[str, BufferedReader]:
        """Converts a list of file paths to file objects.

        Converts a list of file paths to file objects. Used by post() method to post files to ActiveCollab

        :param list[str] attachments: List of file paths
        :return: dictionary of filenames (key) and file objects (value).
        :rtype: dict[str, BufferedReader]
        """
        if attachments is None:
            raise InvalidArgumentError("No attachments provided")
        file_params = {}

        if attachments:
            counter = 1

            for attachment in attachments:
                path = attachment[0] if type(attachment) is list else attachment

                if not os.path.isfile(path):
                    raise FileNotFoundError(f'{path} not found')

                with open(path, 'rb') as file:
                    file_params[f'attachment_{counter}'] = file
                    counter +=1

        return file_params

    def info(self, property: Any = False):
        """Retrieves a cached info response

        :param Any property: Flag
        :return: Cached info response if succesful; False otherwise
        :rtype: str|bool
        """

        if not self.info_response and type(self.info_response) is bool:
            self.info_response = self.get('info').json()
        
        if type(property) is not bool:
            return self.info_response[property] or None
        else:
            return self.info_response

    def get(self, url: str) -> Response:
        """HTTP Get request to ActiveCollab

            Makes a get request to active collab using the provided URL

            :param str url: URL to send get request.
            :raise: SystemExit() on failure
            :return: HTTP response
            :rtype: Response
        
        """
        try:
            r = requests.get(url=self._prepare_url(url), headers=self.header)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e) from e

        return r

    def post(self, url: str, params: dict, attachments: list[str] = []) -> None:
        """HTTP Post request to ActiveCollab (Create New)

            Makes a post request to ActiveCollab using the provided URL, parameters/data, and attachments (optional)

            :param str url: URL to make post request.
            :param dict param: Data to post to ActiveCollab.
            :param list[str] attachments: Data to post to ActiveCollab.
            :raise: SystemExit() on request, connection, or HTTP failure
            :return: HTTP response
            :rtype: Response
        
        """
        try:

            r = requests.post(url=self._prepare_url(url), json=params, headers=self.header, files=self._prepare_files(attachments))
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e) from e

    def put(self, url: str, params: dict) -> None:
        """HTTP Put request from ActiveCollab (Insert/Replace)

            Makes a get request to active collab using the provided URL

            :param str url: URL to send get request.
            :param dict params: parameters to put to ActiveCollab
            :raise: SystemExit() on request, connection, or HTTP failure
            :return:
            :rtype: None
        """
        try:

            r = requests.put(url=self._prepare_url(url), json=params, headers=self.header)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
                raise SystemExit(e) from e

    def delete(self, url:str) -> None:
        """HTTP Delete request from ActiveCollab

            Makes a delete request to ActiveCollab using the provided URL and parameters

            :param str url: URL to send get request.
            :param dict params: parameters to delete from ActiveCollab
            :raise: SystemExit() on request, connection, or HTTP failure
            :return:
            :rtype: None
        """
        try:
            r = requests.delete(url = self._prepare_url(url), headers=self.header)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
                raise SystemExit(e) from e