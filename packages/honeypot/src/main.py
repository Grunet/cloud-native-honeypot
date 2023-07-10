import signal
import os

from servers import simple_http
from servers.server_adapter_protocol import ServerAdapterProtocol


def isServerEnabled(envVarName: str) -> bool:
    envVarValue = os.environ.get(envVarName)

    if (envVarValue is not None) & (len(envVarValue) > 0):
        return True

    return False


if __name__ == "__main__":
    serverAdapters: list[ServerAdapterProtocol] = []

    def terminationHandler(sig, frame):
        for serverAdapter in serverAdapters:
            serverAdapter.stop()

        print("Exiting the process")

    signal.signal(signal.SIGINT, terminationHandler)
    signal.signal(signal.SIGTERM, terminationHandler)

    if isServerEnabled("ENABLE_SIMPLE_HTTP"):
        sa = simple_http.createServerAdapter()
        serverAdapters.append(sa)

    for serverAdapter in serverAdapters:
        serverAdapter.start()
