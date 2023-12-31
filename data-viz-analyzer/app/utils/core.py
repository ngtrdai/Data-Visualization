from enum import IntEnum, Enum
from typing import NamedTuple, Union

from sqlalchemy import URL, make_url
from sqlalchemy.sql.type_api import TypeEngine


class GenericDataType(IntEnum):
    NUMERIC = 0
    STRING = 1
    TEMPORAL = 2
    BOOLEAN = 3


class ColumnTypeSource(Enum):
    GET_TABLE = 1
    CURSOR_DESCRIPTION = 2


class ColumnSpec(NamedTuple):
    sqla_type: TypeEngine | str
    generic_type: GenericDataType
    is_dttm: bool
    python_date_format: str | None = None


def make_url_safe(raw_url: Union[str, URL]) -> URL:
    if isinstance(raw_url, str):
        url = raw_url.strip()
        try:
            return make_url(url)
        except Exception:
            raise ValueError(f"Invalid URL: {url}")

    return raw_url
