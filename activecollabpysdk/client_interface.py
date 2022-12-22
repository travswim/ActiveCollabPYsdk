from abc import ABCMeta, abstractmethod
from typing import Any


class ClientInterface(metaclass=ABCMeta):
    """Base class for Client"""

    def __init__(self) -> None:
        self.__version = '3.0.0'

    @abstractmethod
    def info(self, property: Any = False):
        pass

    @abstractmethod
    def get(self, url: str) -> str:
        pass

    @abstractmethod
    def post(
        self, url: str,
        params: dict = {},
        attachments: list[str] = []
    ) -> None:
        pass

    @abstractmethod
    def put(self, url: str, params: dict = {}):
        pass

    @abstractmethod
    def delete(self, url: str, params: dict) -> None:
        pass