import signal
import os
from typing import Any

from event_clients.event_client_adapter_protocol import EventClientAdapterProtocol
from event_clients.eventbridge_client_adapter import (
    create_event_client_adapter,
    EventbridgeClientAdapterInputs,
)
from servers import simple_http
from servers.server_adapter_protocol import ServerAdapterProtocol

server_name_to_env_var_dict = {"simple_http": "ENABLE_SERVER_SIMPLE_HTTP"}


class ServerAdaptersManager:
    def __init__(self) -> None:
        self.__server_adapters: list[ServerAdapterProtocol] = []

    def start_servers(self) -> None:
        event_client = try_create_eventbrige_client()

        if is_server_enabled("simple_http"):
            sa = simple_http.create_server_adapter(
                simple_http.ServerAdapterInputs(event_client=event_client)
            )
            self.__server_adapters.append(sa)

        for server_adapter in self.__server_adapters:
            server_adapter.start()

    def stop_servers(self) -> None:
        for server_adapter in self.__server_adapters:
            server_adapter.stop()


def try_create_eventbrige_client() -> EventClientAdapterProtocol | None:
    if not is_environment_variable_truthy("ENABLE_EVENT_CLIENT_EVENTBRIDGE"):
        return None

    try:
        event_bus_name_or_arn = os.environ.get("EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN")

        if not event_bus_name_or_arn:
            print("Missing EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN")
            return None

        return create_event_client_adapter(
            EventbridgeClientAdapterInputs(event_bus_name_or_arn=event_bus_name_or_arn)
        )
    except Exception as ex:
        print("Failed to create eventbridge client")
        print(ex)
        return None


def is_server_enabled(serverName: str) -> bool:
    env_var_name = server_name_to_env_var_dict[serverName]

    return is_environment_variable_truthy(env_var_name)


def is_environment_variable_truthy(env_var_name: str) -> bool:
    env_var_value = os.environ.get(env_var_name)

    if (env_var_value) and (len(env_var_value) > 0):
        return True

    return False


if __name__ == "__main__":
    server_adapters_manager = ServerAdaptersManager()

    def termination_handler(sig: int, frame: Any) -> None:
        server_adapters_manager.stopServers()

        print("Exiting the process")

    signal.signal(signal.SIGINT, termination_handler)
    signal.signal(signal.SIGTERM, termination_handler)

    server_adapters_manager.startServers()
