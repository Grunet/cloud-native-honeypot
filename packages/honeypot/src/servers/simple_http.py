from . import server_adapter_protocol


class SimpleHttpServerAdapter(server_adapter_protocol.ServerAdapterProtocol):
    def start(self):
        print("start")
        pass

    def stop(self):
        print("stop")
        pass


def createServerAdapter() -> server_adapter_protocol.ServerAdapterProtocol:
    return SimpleHttpServerAdapter()
