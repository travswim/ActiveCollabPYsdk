from typing import Any
from authenticator import Authenticator
from urllib.parse import urlparse
from Exceptions import AuthenticationError, InvalidArgumentError
import requests

class SelfHosted(Authenticator):
    """Self hosted interface for ActiveCollab"""

    def __init__(self, your_org_name: str, your_app_name: str, email_address: str, password: str, self_hosted_url: str, api_version: int) -> None:
        super().__init__(your_org_name, your_app_name, email_address, password)

        result = urlparse(self_hosted_url)

        if not all([result.scheme, result.netloc]):
            raise InvalidArgumentError(f'Self hoste URL {self_hosted_url} is not valid')
        self.self_hosted_url = self_hosted_url

        if api_version <= 0:
            raise InvalidArgumentError(f'{api_version} is an invalid api version')
        self.api_versionself_hosted_url = api_version
            

    def issueToken(self):
        """Issues a token for a self hosted ActiveCollab acocunt

        :raise: SystemExit() on request, connection, or HTTP failure
        :raise: AuthenticationError() on an invalid json response
        :return: A Token object
        :rtype: Token
        """

        request_url = f'{self.self_hosted_url}/api/v{self.api_versionself_hosted_url}/issue-token'

        data =  {
            'username': self.email_address,
            'password': self.password,
            'client_name': self.app_name,
            'client_vendor': self.org_name
        }
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

        try:
            r = requests.post(request_url, json=data, headers=headers)
            r.raise_for_status()  
        except requests.HTTPError as e:
            raise SystemExit(e)

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        # Request JSON received
        if r.json() and r.headers['content-type'] == 'application/json':
            
            response = r.json()

            if not response['is_ok'] or not response['token']:
                contentType = r.headers['content-type']
                raise AuthenticationError(f'Invalid response from {request_url}. JSON expected, got {contentType}, status code {r.status_code}')
            
            return self.issueTokenResponseToToken(r, self.self_hosted_url)