from .simple_http import create_server_adapter, ServerAdapterInputs

import unittest
import http.client


class TestSimpleHttpServerAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.__server_adapter = create_server_adapter(
            ServerAdapterInputs(eventClient=None)
        )

    def tearDown(self) -> None:
        # Here for cleanup regardless of what happens during a test
        self.__server_adapter.stop()

    def test_GET_returns_200(self) -> None:
        # Arrange
        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        # Act
        self.__server_adapter.start()

        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        status_code = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
