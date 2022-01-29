from urllib.parse import urlparse
from activecollabpysdk.Exceptions import InvalidArgumentError
from dataclasses import dataclass  

@dataclass
class Token:
    """A dataclass for tokens"""
    token: str
    url: str

    def __post_init__(self):
        """
        validate the assigned url & token
        """
        result = urlparse(self.url)

        if not all([result.scheme, result.netloc]):
            raise InvalidArgumentError(f'{self.url} is not a valid URL')

        if not self.token:
            raise InvalidArgumentError('Empty token')

    def __str__(self) -> str:
        return f'Token: {self.token}\n URL: {self.url}'
        