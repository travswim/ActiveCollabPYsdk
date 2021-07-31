from typing import Any
import validators
from Exceptions import InvalidArgumentError
from dataclasses import dataclass   

@dataclass
class Tokens:

    token: str
    url: str

    def __post_init__(self):
        if not validators.url(Any(self.url)):
            raise InvalidArgumentError(f'{self.url} is not a valid URL')

    def __str__(self) -> str:
        return f'Token: {self.token}\n URL: {self.url}'