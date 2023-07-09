from server_adapter_protocol import ServerAdapterProtocol


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def start(self):
        pass

    def stop(self):
        pass


def createServerAdapter() -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter()
