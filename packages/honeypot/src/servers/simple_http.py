from .server_adapter_protocol import ServerAdapterProtocol


class SimpleHttpServerAdapter(ServerAdapterProtocol):
    def start(self):
        print("start")
        pass

    def stop(self):
        print("stop")
        pass


def createServerAdapter() -> ServerAdapterProtocol:
    return SimpleHttpServerAdapter()
