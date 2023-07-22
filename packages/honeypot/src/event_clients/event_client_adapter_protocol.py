from typing import Protocol
from abc import abstractmethod


class EventClientAdapterProtocol(Protocol):
    @abstractmethod
    def send_event(self, event_details: object) -> None:
        raise NotImplementedError
