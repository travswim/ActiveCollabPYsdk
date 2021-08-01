from requests.models import Response
from Exceptions import AuthenticationError
from typing import Any
import validators
from authenticator_interface import AuthenticatorInterface
from token_sdk import Token

class Authenticator(AuthenticatorInterface):
    """A class for authenticating a user with a Token"""
    
    def __init__(self, your_org_name: str, your_app_name: str, email_address: str, password: str) -> None:
        
        self.org_name: str = your_org_name
        self.app_name: str = your_app_name
        if not validators.email(Any(email_address)):
            raise ValueError('Not a valid email address')
        self.email_address: str = email_address         
        self.password: str = password

    def issueTokenResponseToToken(self, response: Response, url: str) -> Token:
        """Issues a token response given a JSON response an url

        Args:
            response ([type]): [description]
            url ([type]): [description]

        Raises:
            AuthenticationError: [description]

        Returns:
            [type]: [description]
        """
        result = response.json()

        if not result['is_ok'] or not result['token']:
            raise AuthenticationError('Authentication rejected')

        return Token(result['token'], url)