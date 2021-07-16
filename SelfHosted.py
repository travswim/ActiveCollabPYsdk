from Authenticator import Authenticator
import validators
from Exceptions import AuthenticationError, InvalidArgumentError
import requests

class SelfHosted(Authenticator):

    def __init__(self, your_org_name: str, your_app_name: str, email_address: str, password: str, self_hosted_url: str, api_version: int) -> None:
        super().__init__(your_org_name, your_app_name, email_address, password)

        if validators.url(self_hosted_url):
            self.__self_hosted_url = self_hosted_url
        else:
            raise InvalidArgumentError("Self hoste URL is not valid")
        
        if api_version > 0:
            self.__api_version = api_version
        else:
            raise InvalidArgumentError("Invalid api version")

    
    def issueToken(self):
        request_url = f'{self.__self_hosted_url}/api/v{self.__api_version}/issue-token'

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
                raise AuthenticationError("Authentication rejected")

            else:
                return