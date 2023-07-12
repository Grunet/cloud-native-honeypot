from .server_adapter_protocol import ServerAdapterProtocol

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def __init__(self) -> None:
        self.__httpServer: HTTPServer | None = None

    def start(self) -> None:
        print("Starting simple HTTP server on port 8000")

        self.__httpServer = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)

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


def createServerAdapter() -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter()
