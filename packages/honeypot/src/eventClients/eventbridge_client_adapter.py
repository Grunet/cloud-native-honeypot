from .event_client_adapter_protocol import EventClientAdapterProtocol


class EventbridgeClientAdapter(EventClientAdapterProtocol):
    def __init__(self) -> None:
        raise NotImplementedError

    def sendEvent(self, eventDetails: object) -> None:
        raise NotImplementedError


def createEventClientAdapter() -> EventClientAdapterProtocol:
    return EventbridgeClientAdapter()
