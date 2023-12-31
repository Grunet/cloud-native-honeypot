from .simple_http import (
    create_server_adapter,
    ServerAdapterInputs,
)
from .server_adapter_protocol import ServerAdapterProtocol
from event_clients.event_client_adapter_protocol import EventClientAdapterProtocol
from telemetry.telemetry_manager_protocol import TelemetryManagerProtocol

import unittest
import http.client


class TestSimpleHttpServerAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.__server_adapter: ServerAdapterProtocol = create_server_adapter(
            ServerAdapterInputs(
                telemetry_manager=create_stub_telemetry_manager(), event_client=None
            )
        )

    def tearDown(self) -> None:
        # Here for cleanup regardless of what happens during a test
        self.__server_adapter.stop()

    def test_GET_returns_200(self) -> None:
        # Arrange
        # server_adapter setup in setUp

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
            ServerAdapterInputs(
                telemetry_manager=create_stub_telemetry_manager(),
                event_client=mock_event_client,
            )
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


def create_stub_telemetry_manager() -> TelemetryManagerProtocol:
    class StubTelemetryManager:
        def record_transaction_detail(self, structured_data: dict[str, object]) -> None:
            pass

        def record_non_transaction_detail(
            self, structured_data: dict[str, object]
        ) -> None:
            pass

    return StubTelemetryManager()


if __name__ == "__main__":
    unittest.main()
