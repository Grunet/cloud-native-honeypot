from typing import Protocol
from abc import abstractmethod


class ServerAdapterProtocol(Protocol):
    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
