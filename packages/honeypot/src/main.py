import signal
import sys

from servers import simple_http
from servers.server_adapter_protocol import ServerAdapterProtocol


if __name__ == "__main__":
    serverAdapters: list[ServerAdapterProtocol] = []

    # TODO - use an environment variable here instead
    if True:
        sa = simple_http.createServerAdapter()
        serverAdapters.append(sa)

    for serverAdapter in serverAdapters:
        serverAdapter.start()

    def terminationHandler():
        for serverAdapter in serverAdapters:
            serverAdapter.stop()

        sys.exit(0)

    signal.signal(signal.SIGINT, terminationHandler)
    signal.signal(signal.SIGTERM, terminationHandler)
