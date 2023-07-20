from .simple_http import createServerAdapter, ServerAdapterInputs

import unittest
import http.client


class TestSimpleHttpServerAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.__serverAdapter = createServerAdapter(
            ServerAdapterInputs(eventClient=None)
        )
        self.__serverAdapter.start()

    def tearDown(self) -> None:
        self.__serverAdapter.stop()

    def test_GET_returns_200(self) -> None:
        # Arrange
        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        # Act
        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        statusCode = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(statusCode, 200)


if __name__ == "__main__":
    unittest.main()
