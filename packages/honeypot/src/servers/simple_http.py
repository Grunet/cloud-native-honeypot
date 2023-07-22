from .server_adapter_protocol import ServerAdapterProtocol
from event_clients.event_client_adapter_protocol import EventClientAdapterProtocol

from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from typing import Any


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request: Any, client_address: Any, server: Any) -> None:
        self.__event_client: EventClientAdapterProtocol | None = server.event_client

        super().__init__(request, client_address, server)

    def do_GET(self) -> None:
        if self.__event_client:
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
                print("Failed to send event in response to GET request")
                print(ex)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def __init__(self, event_client: EventClientAdapterProtocol | None) -> None:
        self.__event_client: EventClientAdapterProtocol | None = event_client

        self.__http_server: HTTPServer | None = None

    def start(self) -> None:
        print("Starting simple HTTP server on port 8000")

        self.__http_server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
        # Only clear way to inject the client into request handling
        # is by appending it onto the server object
        # and reading it later on
        event_client = self.__event_client  # gets around next line length limit
        self.__http_server.event_client = event_client  # type: ignore[attr-defined]

        def start_in_separate_thread(http_server: HTTPServer | None) -> None:
            if http_server:
                http_server.serve_forever()

        thread = Thread(target=start_in_separate_thread, args=(self.__http_server,))
        thread.start()

    def stop(self) -> None:
        print("Stopping simple HTTP server")

        def stop_in_separate_thread(http_server: HTTPServer | None) -> None:
            if http_server:
                http_server.shutdown()

        thread = Thread(target=stop_in_separate_thread, args=(self.__http_server,))
        thread.start()
        thread.join()


@dataclass
class ServerAdapterInputs:
    event_client: EventClientAdapterProtocol | None


def create_server_adapter(inputs: ServerAdapterInputs) -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter(event_client=inputs.event_client)
