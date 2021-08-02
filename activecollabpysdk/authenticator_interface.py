from abc import ABCMeta, abstractmethod
from requests.models import Response
from token_sdk import Token

class AuthenticatorInterface(meta=ABCMeta):
    """Base class for Authentication"""

    @abstractmethod
    def issueTokenResponseToToken(self, response: Response, url: str) -> Token:
        pass
