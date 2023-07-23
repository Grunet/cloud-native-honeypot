from .telemetry_manager_protocol import TelemetryManagerProtocol

import copy
from datetime import datetime, timezone
import json
import sys
import traceback


class TelemetryManager(TelemetryManagerProtocol):
    def record_transaction_detail(self, structured_data: dict[str, object]) -> None:
        try:
            self.__record_detail(structured_data=structured_data)
        except Exception:
            pass

    def record_non_transaction_detail(self, structured_data: dict[str, object]) -> None:
        try:
            self.__record_detail(structured_data=structured_data)
        except Exception:
            pass

    def __record_detail(self, structured_data: dict[str, object]) -> None:
        cloned_data = copy.deepcopy(structured_data)

        current_time = datetime.now(timezone.utc)
        formatted_time = current_time.isoformat()
        cloned_data["timestamp"] = formatted_time

        if "exception" in cloned_data:
            stack_trace = traceback.format_exc()
            cloned_data["stackTrace"] = stack_trace

        if "exception" in cloned_data:
            # Some exceptions are not json serializable as is
            cloned_data["exception"] = str(cloned_data["exception"])

        data_as_json = json.dumps(cloned_data, indent=4, sort_keys=True)

        sys.stdout.write(data_as_json)
        sys.stdout.write("\n")
        sys.stdout.flush()


def create_telemetry_manager() -> TelemetryManagerProtocol:
    return TelemetryManager()
