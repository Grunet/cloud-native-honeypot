from .server_adapter_protocol import ServerAdapterProtocol

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


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

        def stop_in_separate_thread(httpServer: HTTPServer | None):
            if httpServer:
                # httpServer.__shutdown_request = True
                # TODO - figure out why this is still blocking/deadlocking the main thread
                httpServer.shutdown()

        thread = Thread(target=stop_in_separate_thread, args=(self.__httpServer,))
        thread.start()
        thread.join()

        print("SOS")


def createServerAdapter() -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter()
