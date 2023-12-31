from dataclasses import dataclass
from enum import StrEnum
from typing import Optional, Any


class DataVizErrorType(StrEnum):
    # DB Engine errors
    GENERIC_DB_ENGINE_ERROR = "GENERIC_DB_ENGINE_ERROR"
    COLUMN_DOES_NOT_EXIST_ERROR = "COLUMN_DOES_NOT_EXIST_ERROR"
    TABLE_DOES_NOT_EXIST_ERROR = "TABLE_DOES_NOT_EXIST_ERROR"
    SCHEMA_DOES_NOT_EXIST_ERROR = "SCHEMA_DOES_NOT_EXIST_ERROR"
    CONNECTION_INVALID_USERNAME_ERROR = "CONNECTION_INVALID_USERNAME_ERROR"
    CONNECTION_INVALID_PASSWORD_ERROR = "CONNECTION_INVALID_PASSWORD_ERROR"
    CONNECTION_INVALID_HOSTNAME_ERROR = "CONNECTION_INVALID_HOSTNAME_ERROR"
    CONNECTION_PORT_CLOSED_ERROR = "CONNECTION_PORT_CLOSED_ERROR"
    CONNECTION_INVALID_PORT_ERROR = "CONNECTION_INVALID_PORT_ERROR"
    CONNECTION_HOST_DOWN_ERROR = "CONNECTION_HOST_DOWN_ERROR"
    CONNECTION_ACCESS_DENIED_ERROR = "CONNECTION_ACCESS_DENIED_ERROR"
    CONNECTION_UNKNOWN_DATABASE_ERROR = "CONNECTION_UNKNOWN_DATABASE_ERROR"
    CONNECTION_DATABASE_PERMISSIONS_ERROR = "CONNECTION_DATABASE_PERMISSIONS_ERROR"
    CONNECTION_MISSING_PARAMETERS_ERROR = "CONNECTION_MISSING_PARAMETERS_ERROR"
    OBJECT_DOES_NOT_EXIST_ERROR = "OBJECT_DOES_NOT_EXIST_ERROR"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    CONNECTION_DATABASE_TIMEOUT = "CONNECTION_DATABASE_TIMEOUT"


class ErrorLevel(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


ISSUE_CODES = {}


ERROR_TYPES_TO_ISSUE_CODES_MAPPING = {}


@dataclass
class DataVizError:
    message: str
    error_type: DataVizErrorType
    level: ErrorLevel
    extra: Optional[dict[str, Any]] = None

    def __post_init__(self) -> None:
        if issue_codes := ERROR_TYPES_TO_ISSUE_CODES_MAPPING.get(self.error_type):
            self.extra = self.extra or {}
            self.extra.update(
                {
                    "issue_codes": [
                        {
                            "code": issue_code,
                            "message": (
                                f"Issue {issue_code} - {ISSUE_CODES[issue_code]}"
                            ),
                        }
                        for issue_code in issue_codes
                    ]
                }
            )

    def to_dict(self) -> dict[str, Any]:
        rv = {"message": self.message, "error_type": self.error_type}
        if self.extra:
            rv["extra"] = self.extra  # type: ignore
        return rv
