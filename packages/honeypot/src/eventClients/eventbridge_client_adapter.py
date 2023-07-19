from .event_client_adapter_protocol import EventClientAdapterProtocol

import boto3

import json


class EventbridgeClientAdapter(EventClientAdapterProtocol):
    def __init__(self) -> None:
        self.__eventbridgeClient = boto3.client("events")

    def sendEvent(self, eventDetails: object) -> None:
        response = self.__eventbridgeClient.put_events(
            Entries=[
                {
                    "Source": "cloud-native-honeypot",
                    "DetailType": "cloudNativeHoneypotTriggered",
                    "Detail": json.dumps(eventDetails),
                    "EventBusName": "default",
                }
            ]
        )

        if response["FailedEntryCount"] == 0:
            print("Event published successfully.")
        else:
            print(f"Failed to publish {response['FailedEntryCount']} event(s).")


def createEventClientAdapter() -> EventClientAdapterProtocol:
    return EventbridgeClientAdapter()
