from typing import Protocol
from abc import abstractmethod


class ServerAdapterProtocol(Protocol):
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
