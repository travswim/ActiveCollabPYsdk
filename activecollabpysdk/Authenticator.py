from requests.models import Response
from email.utils import parseaddr

from activecollabpysdk.Exceptions import AuthenticationError
from activecollabpysdk.authenticator_interface import AuthenticatorInterface
from activecollabpysdk.token_sdk import Token

class Authenticator(AuthenticatorInterface):
    """A class for authenticating a user with a Token"""
    
    def __init__(self, your_org_name: str, your_app_name: str, email_address: str, password: str) -> None:
        
        self.org_name: str = your_org_name
        self.app_name: str = your_app_name
        valid_email = parseaddr(email_address)
        if valid_email[0] == valid_email[1] == '':
            raise ValueError('Not a valid email address')
        self.email_address: str = email_address         
        self.password: str = password
        

    def issueTokenResponseToToken(self, response: Response, url: str) -> Token:
        """
        Issues a token to the user

        :param response [Response]: The response from the server
        :param url [str]: The url of the server

        :return: A token object

        """
        result = response.json()
        print(response.content)
        if not result['is_ok'] or not result['token']:
            raise AuthenticationError('Authentication rejected')

        return Token(result['token'], url)