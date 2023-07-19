from typing import Protocol
from abc import abstractmethod


class EventClientAdapterProtocol(Protocol):
    @abstractmethod
    def sendEvent(self, eventDetails: object) -> None:
        raise NotImplementedError
