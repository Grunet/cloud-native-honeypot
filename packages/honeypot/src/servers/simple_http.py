from .server_adapter_protocol import ServerAdapterProtocol
from event_clients.event_client_adapter_protocol import EventClientAdapterProtocol
from telemetry.telemetry_manager_protocol import TelemetryManagerProtocol

from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from typing import Any


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request: Any, client_address: Any, server: Any) -> None:
        self.__telemetry_manager: TelemetryManagerProtocol = server.telemetry_manager
        self.__event_client: EventClientAdapterProtocol | None = server.event_client

        super().__init__(request, client_address, server)

    # Not overriding log_message to use telemetry_manager
    # Too complex/risky for not enough benefit at the moment

    def do_GET(self) -> None:
        is_healthcheck = (self.path == "/healthcheck") or (self.path == "/healthcheck/")
        if is_healthcheck:
            self.__telemetry_manager.record_transaction_detail(
                {"message": "Healthcheck route hit", "level": "DEBUG"}
            )

        should_publish_event = not is_healthcheck

        if self.__event_client and should_publish_event:
            try:
                self.__event_client.send_event(
                    {
                        "server": "simple_http",
                        "requestMethod": "GET",
                        "clientIp": self.client_address[0],
                        "userAgent": self.headers.get("User-Agent"),
                    }
                )
            except Exception as ex:
                self.__telemetry_manager.record_transaction_detail(
                    {
                        "message": "Failed to send event in response to GET request",
                        "level": "ERROR",
                        "exception": ex,
                    }
                )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def __init__(
        self,
        telemetry_manager: TelemetryManagerProtocol,
        event_client: EventClientAdapterProtocol | None,
    ) -> None:
        self.__telemetry_manager = telemetry_manager
        self.__event_client: EventClientAdapterProtocol | None = event_client

        self.__http_server: HTTPServer | None = None

    def start(self) -> None:
        self.__telemetry_manager.record_non_transaction_detail(
            {"message": "Starting simple HTTP server on port 8000", "level": "INFO"}
        )

        self.__http_server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
        # Only clear way to inject the client into request handling
        # is by appending it onto the server object
        # and reading it later on
        tm = self.__telemetry_manager  # gets around next line length limit
        self.__http_server.telemetry_manager = tm  # type: ignore[attr-defined]
        ec = self.__event_client  # gets around next line length limit
        self.__http_server.event_client = ec  # type: ignore[attr-defined]

        def start_in_separate_thread(http_server: HTTPServer | None) -> None:
            if http_server:
                http_server.serve_forever()

        thread = Thread(target=start_in_separate_thread, args=(self.__http_server,))
        thread.start()

    def stop(self) -> None:
        self.__telemetry_manager.record_non_transaction_detail(
            {"message": "Stopping simple HTTP server", "level": "INFO"}
        )

        def stop_in_separate_thread(http_server: HTTPServer | None) -> None:
            if http_server:
                http_server.shutdown()

        thread = Thread(target=stop_in_separate_thread, args=(self.__http_server,))
        thread.start()
        thread.join()


@dataclass
class ServerAdapterInputs:
    telemetry_manager: TelemetryManagerProtocol
    event_client: EventClientAdapterProtocol | None


def create_server_adapter(inputs: ServerAdapterInputs) -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter(
        telemetry_manager=inputs.telemetry_manager, event_client=inputs.event_client
    )
