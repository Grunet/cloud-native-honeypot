from .simple_http import createServerAdapter

import unittest
import http.client


class TestSimpleHttpServerAdapter(unittest.TestCase):
    def setUp(self):
        self.__serverAdapter = createServerAdapter()
        self.__serverAdapter.start()

    def tearDown(self):
        self.__serverAdapter.stop()

    def test_GET_returns_200(self):
        # Arrange
        conn = http.client.HTTPConnection("127.0.0.1:8000")

        # Act
        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        statusCode = response.getcode()
        conn.close()

        self.assertEqual(statusCode, 200)


if __name__ == "__main__":
    unittest.main()
