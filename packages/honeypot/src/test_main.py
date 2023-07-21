from main import ServerAdaptersManager

import unittest
import http.client
import os

import boto3
from moto import mock_events


class TestServerAdaptersManager(unittest.TestCase):
    def setUp(self) -> None:
        self.__serverAdaptersManager = ServerAdaptersManager()

    def tearDown(self) -> None:
        # Here for cleanup regardless of what happens during a test
        self.__serverAdaptersManager.stopServers()

        del os.environ["ENABLE_SERVER_SIMPLE_HTTP"]

    @mock_events
    def test_GET_to_simple_http_publishes_to_eventbridge(self) -> None:
        # Arrange
        os.environ["ENABLE_SERVER_SIMPLE_HTTP"] = "true"

        os.environ["ENABLE_EVENT_CLIENT_EVENTBRIDGE"] = "true"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

        eventbridgeClient = boto3.client("events")
        eventBusArn = eventbridgeClient.create_event_bus(Name="test_bus")["EventBusArn"]

        os.environ["EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN"] = eventBusArn

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
