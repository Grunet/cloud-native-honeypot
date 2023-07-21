from main import ServerAdaptersManager

import unittest
import http.client
import os
import json

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
    def test_GET_to_simple_http_publishes_event_to_eventbridge(self) -> None:
        # Arrange
        os.environ["ENABLE_SERVER_SIMPLE_HTTP"] = "true"

        os.environ["ENABLE_EVENT_CLIENT_EVENTBRIDGE"] = "true"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"  # Choice is unimportant

        eventbridgeClient = boto3.client("events")
        eventBusArn = eventbridgeClient.create_event_bus(Name="unused")["EventBusArn"]

        os.environ["EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN"] = eventBusArn

        archiveName = "eventBusArchive"
        eventbridgeClient.create_archive(
            ArchiveName=archiveName,
            EventSourceArn=eventBusArn,
            EventPattern=json.dumps(
                {"source": ["cloud-native-honeypot"]}
            ),  # This is implicitly part of the assertions
        )

        # Act
        self.__serverAdaptersManager.startServers()

        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        statusCode = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(statusCode, 200)

        eventCount = eventbridgeClient.describe_archive(ArchiveName=archiveName)[
            "EventCount"
        ]
        self.assertEqual(eventCount, 1)