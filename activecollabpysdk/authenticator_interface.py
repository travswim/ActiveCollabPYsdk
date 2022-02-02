from abc import ABCMeta, abstractmethod
from requests.models import Response
from activecollabpysdk.token_sdk import Token

class AuthenticatorInterface(metaclass=ABCMeta):
    """Base class for Authentication"""

    @abstractmethod
    def issueTokenResponseToToken(self, response: Response, url: str) -> Token:
        pass
