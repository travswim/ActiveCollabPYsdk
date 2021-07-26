from Exceptions import AuthenticationError
import re
from typing import Any
import validators
from Token import Token

class Authenticator:
    
    def __init__(self, your_org_name: str, your_app_name: str, email_address: str, password: str) -> None:
        
        self.__org_name: str = your_org_name
        self.__app_name: str = your_app_name
        if validators.email(Any(email_address)):
            self.__email_address: str = email_address
        else:
            raise ValueError('Not a valid email address')
        self.__password: str = password
    
    # Getter/setter functions for Organization Name
    @property
    def org_name(self) -> str:
        return self.__org_name

    @org_name.setter
    def org_name(self, name: str) -> None:
        if not name:
            raise ValueError('Requires an organization name')
        self.__org_name = name


    # Getter/setter function for Application Name
    @property
    def app_name(self) -> str:
        return self.__app_name

    @app_name.setter
    def app_name(self, name: str) -> None:
        if not name:
            raise ValueError('You require an application name')
        self.__app_name = name
    

    # Getter/setter function for Account Email Address
    @property
    def email_address(self) -> str:
        return self.__email_address

    @email_address.setter
    def email_address(self, email) -> None:
        if not email:
            raise ValueError('You require an email address')
        elif type(email) is not str:
            raise ValueError('Wrong type, email should be of type() str')
        elif not validators.email(email):
            raise ValueError('Not a valide email')

        else:
            self.__email_address = email

    # Getter/setter function for Account Password
    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, your_password: str) -> None:
        if not your_password:
            raise ValueError('You require an application name')
        self.__password = your_password


    def issueTokenResponseToToken(self, response, url):
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
        
        else:
        
            return Token(result['token'], url)