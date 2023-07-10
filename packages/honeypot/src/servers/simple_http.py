from .server_adapter_protocol import ServerAdapterProtocol

from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def init(self):
        self.__httpServer: HTTPServer | None = None

    def start(self):
        print("Starting simple HTTP server on port 8000")

        self.__httpServer = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
        self.__httpServer.serve_forever()

    def stop(self):
        print("Stopping simple HTTP server")

        if self.__httpServer:
            self.__httpServer.shutdown()


def createServerAdapter() -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter()
