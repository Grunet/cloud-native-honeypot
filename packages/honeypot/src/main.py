import signal
import os

from servers import simple_http
from servers.server_adapter_protocol import ServerAdapterProtocol

serverNameToEnvVarDict = {"simple_http": "ENABLE_SIMPLE_HTTP"}


def isServerEnabled(serverName: str) -> bool:
    envVarName = serverNameToEnvVarDict[serverName]

    envVarValue = os.environ.get(envVarName)

    if (envVarValue) and (len(envVarValue) > 0):
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

    if isServerEnabled("simple_http"):
        sa = simple_http.createServerAdapter()
        serverAdapters.append(sa)

    for serverAdapter in serverAdapters:
        serverAdapter.start()
