from main import ServerAdaptersManager
from telemetry.telemetry_manager import create_telemetry_manager

import unittest
import http.client
import os
import json

import boto3

# See https://github.com/getmoto/moto/issues/4944 for if the ignore can be removed
from moto import mock_events  # type: ignore[import]


class TestServerAdaptersManager(unittest.TestCase):
    def setUp(self) -> None:
        self.__used_environment_variables = set()

        self.__server_adapters_manager = ServerAdaptersManager(
            telemetry_manager=create_telemetry_manager()
        )

    def tearDown(self) -> None:
        # Here for cleanup regardless of what happens during a test
        self.__server_adapters_manager.stop_servers()

        for environment_variable_name in self.__used_environment_variables:
            del os.environ[environment_variable_name]

    def __set_environment_variable(self, name: str, value: str) -> None:
        os.environ[name] = value

        self.__used_environment_variables.add(name)

    # See https://github.com/getmoto/moto/issues/4944 for if the ignore can be removed
    @mock_events  # type: ignore[misc]
    def test_GET_to_simple_http_publishes_event_to_eventbridge(self) -> None:
        # Arrange
        self.__set_environment_variable("ENABLE_SERVER_SIMPLE_HTTP", "true")

        self.__set_environment_variable("ENABLE_EVENT_CLIENT_EVENTBRIDGE", "true")
        self.__set_environment_variable("AWS_DEFAULT_REGION", "us-east-1")

        eventbridge_client = boto3.client("events")
        event_bus_arn = eventbridge_client.create_event_bus(Name="unused")[
            "EventBusArn"
        ]

        self.__set_environment_variable(
            "EVENTBRIDGE_EVENT_BUS_NAME_OR_ARN", event_bus_arn
        )

        archive_name = "eventBusArchive"
        eventbridge_client.create_archive(
            ArchiveName=archive_name,
            EventSourceArn=event_bus_arn,
            EventPattern=json.dumps(
                {"source": ["cloud-native-honeypot"]}
            ),  # This is implicitly part of the assertions
        )

        conn = http.client.HTTPConnection("127.0.0.1:8000", timeout=5)

        # Act
        self.__server_adapters_manager.start_servers()

        conn.request("GET", "/")

        # Assert
        response = conn.getresponse()
        status_code = response.getcode()
        conn.close()  # unittest reports an unclosed socket even with this

        self.assertEqual(status_code, 200)

        event_count = eventbridge_client.describe_archive(ArchiveName=archive_name)[
            "EventCount"
        ]
        self.assertEqual(event_count, 1)
