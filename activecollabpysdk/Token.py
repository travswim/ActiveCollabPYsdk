import validators
from Exceptions import InvalidArgumentError
class Token:

    def __init__(self, token: str, url) -> None:
        self.__token = token
        if validators.url(url):
            self.__url = url
        else:
            raise InvalidArgumentError("Not a valid URL")

    def __str__(self) -> str:
        return f'Token: {self.token}\n URL: {self.url}'

    def __repr__(self) -> str:
        return f'Token: {self.token}\n URL: {self.url}'

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value: str):
        self.__token = value

    @property
    def url(self):
        return self.__url
        
    @url.setter
    def url(self, value):
        if validators.url(value):
            self.__url = value
        else:
            raise InvalidArgumentError("Not a valid URL")
