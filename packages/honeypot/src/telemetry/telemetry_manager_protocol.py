from typing import Protocol
from abc import abstractmethod


class TelemetryManagerProtocol(Protocol):
    @abstractmethod
    def record_transaction_detail(self, structured_data: dict[str, object]) -> None:
        raise NotImplementedError

    @abstractmethod
    def record_non_transaction_detail(self, structured_data: dict[str, object]) -> None:
        raise NotImplementedError
