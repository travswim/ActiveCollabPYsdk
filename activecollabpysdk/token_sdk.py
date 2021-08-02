import validators
from Exceptions import InvalidArgumentError
from dataclasses import dataclass   

@dataclass
class Token:
    """A dataclass for tokens"""
    token: str
    url: str

    def __post_init__(self):
        if not validators.url(self.url):
            raise InvalidArgumentError(f'{self.url} is not a valid URL')

    def __str__(self) -> str:
        return f'Token: {self.token}\n URL: {self.url}'