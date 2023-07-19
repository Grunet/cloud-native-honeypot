from .event_client_adapter_protocol import EventClientAdapterProtocol

import boto3

from dataclasses import dataclass
import json


class EventbridgeClientAdapter(EventClientAdapterProtocol):
    def __init__(self, **kwargs) -> None:
        self.__eventBusNameOrArn = kwargs.get("eventBusNameOrArn")

        self.__eventbridgeClient = boto3.client("events")

    def sendEvent(self, eventDetails: object) -> None:
        response = self.__eventbridgeClient.put_events(
            Entries=[
                {
                    "Source": "cloud-native-honeypot",
                    "DetailType": "cloudNativeHoneypotTriggered",
                    "Detail": json.dumps(eventDetails),
                    "EventBusName": self.__eventBusNameOrArn,
                }
            ]
        )

        if response["FailedEntryCount"] == 0:
            print("Eventbridge event published successfully.")
        else:
            print(
                f"""Failed to publish {response['FailedEntryCount']} event(s) to
                     Eventbridge."""
            )


@dataclass
class EventbridgeClientAdapterInputs:
    eventBusNameOrArn: str


def createEventClientAdapter(
    inputs: EventbridgeClientAdapterInputs,
) -> EventClientAdapterProtocol:
    eventBusNameOrArn = inputs.eventBusNameOrArn
    if not eventBusNameOrArn:
        raise ValueError("eventBusNameOrArn must be a non-empty string")

    return EventbridgeClientAdapter(eventBusNameOrArn=eventBusNameOrArn)
