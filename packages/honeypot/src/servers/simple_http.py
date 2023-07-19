from .server_adapter_protocol import ServerAdapterProtocol
from eventClients.event_client_adapter_protocol import EventClientAdapterProtocol

from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.__eventClient: EventClientAdapterProtocol | None = server.eventClient

        super().__init__(request, client_address, server)

    def do_GET(self) -> None:
        if self.__eventClient:
            self.__eventClient.sendEvent(
                {
                    "server": "simple_http",
                    "requestMethod": "GET",
                    "clientIp": self.client_address[0],
                    "userAgent": self.headers.get("User-Agent"),
                }
            )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def __init__(self, **kwargs) -> None:
        self.__eventClient = kwargs.get("eventClient")

        self.__httpServer: HTTPServer | None = None

    def start(self) -> None:
        print("Starting simple HTTP server on port 8000")

        self.__httpServer = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
        self.__httpServer.eventClient = self.__eventClient

        def start_in_separate_thread(httpServer: HTTPServer | None) -> None:
            if httpServer:
                httpServer.serve_forever()

        thread = Thread(target=start_in_separate_thread, args=(self.__httpServer,))
        thread.start()

    def stop(self) -> None:
        print("Stopping simple HTTP server")

        def stop_in_separate_thread(httpServer: HTTPServer | None) -> None:
            if httpServer:
                httpServer.shutdown()

        thread = Thread(target=stop_in_separate_thread, args=(self.__httpServer,))
        thread.start()
        thread.join()


@dataclass
class ServerAdapterInputs:
    eventClient: EventClientAdapterProtocol | None


def createServerAdapter(inputs: ServerAdapterInputs) -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter(eventClient=inputs.eventClient)
