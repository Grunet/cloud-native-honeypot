from main import ServerAdaptersManager

import unittest
import http.client
import os


class TestServerAdaptersManager(unittest.TestCase):
    def setUp(self) -> None:
        self.__serverAdaptersManager = ServerAdaptersManager()

    def tearDown(self) -> None:
        # Here for cleanup regardless of what happens during a test
        self.__serverAdaptersManager.stopServers()

        del os.environ["ENABLE_SERVER_SIMPLE_HTTP"]

    def test_GET_to_simple_http_publishes_to_eventbridge(self) -> None:
        # Arrange
        os.environ["ENABLE_SERVER_SIMPLE_HTTP"] = "true"

        self.__serverAdaptersManager.startServers()

        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        # Act
        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        statusCode = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(statusCode, 200)

        # TODO - assert that EventBridge was hit
