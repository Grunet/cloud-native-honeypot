from .event_client_adapter_protocol import EventClientAdapterProtocol

import boto3


class EventbridgeClientAdapter(EventClientAdapterProtocol):
    def __init__(self) -> None:
        self.__eventbridgeClient = boto3.client("events")

    def sendEvent(self, eventDetails: object) -> None:
        raise NotImplementedError


def createEventClientAdapter() -> EventClientAdapterProtocol:
    return EventbridgeClientAdapter()
