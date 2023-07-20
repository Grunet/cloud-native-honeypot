import signal
import os
from typing import Any

from eventClients.event_client_adapter_protocol import EventClientAdapterProtocol
from eventClients.eventbridge_client_adapter import (
    createEventClientAdapter,
    EventbridgeClientAdapterInputs,
)
from servers import simple_http
from servers.server_adapter_protocol import ServerAdapterProtocol

serverNameToEnvVarDict = {"simple_http": "ENABLE_SERVER_SIMPLE_HTTP"}


def isServerEnabled(serverName: str) -> bool:
    envVarName = serverNameToEnvVarDict[serverName]

    return isEnvironmentVariableTruthy(envVarName)


def tryCreateEventbrigeClient() -> EventClientAdapterProtocol | None:
    if not isEnvironmentVariableTruthy("ENABLE_EVENT_CLIENT_EVENTBRIDGE"):
        return None

    try:
        eventBusNameOrArn = os.environ.get("EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN")

        if not eventBusNameOrArn:
            print("Missing EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN")
            return None

        return createEventClientAdapter(
            EventbridgeClientAdapterInputs(eventBusNameOrArn=eventBusNameOrArn)
        )
    except Exception as ex:
        print(ex)
        return None


def isEnvironmentVariableTruthy(envVarName: str) -> bool:
    envVarValue = os.environ.get(envVarName)

    if (envVarValue) and (len(envVarValue) > 0):
        return True

    return False


if __name__ == "__main__":
    serverAdapters: list[ServerAdapterProtocol] = []

    def terminationHandler(sig: int, frame: Any) -> None:
        for serverAdapter in serverAdapters:
            serverAdapter.stop()

        print("Exiting the process")

    signal.signal(signal.SIGINT, terminationHandler)
    signal.signal(signal.SIGTERM, terminationHandler)

    eventClient = tryCreateEventbrigeClient()

    if isServerEnabled("simple_http"):
        sa = simple_http.createServerAdapter(
            simple_http.ServerAdapterInputs(eventClient=eventClient)
        )
        serverAdapters.append(sa)

    for serverAdapter in serverAdapters:
        serverAdapter.start()
