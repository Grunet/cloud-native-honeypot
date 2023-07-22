from .simple_http import (
    create_server_adapter,
    ServerAdapterInputs,
)
from .server_adapter_protocol import ServerAdapterProtocol
from event_clients.event_client_adapter_protocol import EventClientAdapterProtocol

import unittest
import http.client


class TestSimpleHttpServerAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.__server_adapter: ServerAdapterProtocol | None = None

    def tearDown(self) -> None:
        # Here for cleanup regardless of what happens during a test
        if self.__server_adapter:
            self.__server_adapter.stop()

    def test_GET_returns_200(self) -> None:
        # Arrange
        self.__server_adapter = create_server_adapter(
            ServerAdapterInputs(event_client=None)
        )

        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        # Act
        self.__server_adapter.start()

        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        status_code = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(status_code, 200)

    def test_GET_of_healthcheck_returns_200_and_doesnt_publish_an_event(self) -> None:
        # Arrange
        class MockEventClient(EventClientAdapterProtocol):
            def __init__(self) -> None:
                self.send_event_hit = False

            def send_event(self, event_details: object) -> None:
                self.send_event_hit = True

        mock_event_client = MockEventClient()
        self.__server_adapter = create_server_adapter(
            ServerAdapterInputs(event_client=mock_event_client)
        )

        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        # Act
        self.__server_adapter.start()

        conn.request("GET", "/healthcheck")

        # Assert
        response = conn.getresponse()
        status_code = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(status_code, 200)

        self.assertEqual(mock_event_client.send_event_hit, False)


if __name__ == "__main__":
    unittest.main()
