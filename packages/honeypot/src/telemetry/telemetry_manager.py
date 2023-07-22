from .telemetry_manager_protocol import TelemetryManagerProtocol

import json
import sys


class TelemetryManager(TelemetryManagerProtocol):
    def record_transaction_detail(self, structured_data: dict[str, object]) -> None:
        self.__record_detail(structured_data=structured_data)

    def record_non_transaction_detail(self, structured_data: dict[str, object]) -> None:
        self.__record_detail(structured_data=structured_data)

    def __record_detail(self, structured_data: dict[str, object]):
        data_as_json = json.dumps(structured_data)

        sys.stdout.write(data_as_json)
        sys.stdout.write("\n")
        sys.stdout.flush()


def create_telemetry_manager() -> TelemetryManagerProtocol:
    return TelemetryManager()
