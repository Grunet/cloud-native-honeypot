from .event_client_adapter_protocol import EventClientAdapterProtocol

import boto3

from dataclasses import dataclass
import json


class EventbridgeClientAdapter(EventClientAdapterProtocol):
    def __init__(self, event_bus_name_or_arn: str) -> None:
        self.__event_bus_name_or_arn: str = event_bus_name_or_arn

        self.__eventbridge_client = boto3.client("events")

    def send_event(self, event_details: object) -> None:
        response = self.__eventbridge_client.put_events(
            Entries=[
                {
                    "Source": "cloud-native-honeypot",
                    "DetailType": "cloudNativeHoneypotTriggered",
                    "Detail": json.dumps(event_details),
                    "EventBusName": self.__event_bus_name_or_arn,
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
    event_bus_name_or_arn: str


def create_event_client_adapter(
    inputs: EventbridgeClientAdapterInputs,
) -> EventClientAdapterProtocol:
    event_bus_name_or_arn = inputs.event_bus_name_or_arn
    if not event_bus_name_or_arn:
        raise ValueError("event_bus_name_or_arn must be a non-empty string")

    return EventbridgeClientAdapter(event_bus_name_or_arn=event_bus_name_or_arn)
