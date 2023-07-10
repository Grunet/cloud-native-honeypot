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

    # TODO - add keyboard interrupt handling
    # TODO - add SIGTERM handling
