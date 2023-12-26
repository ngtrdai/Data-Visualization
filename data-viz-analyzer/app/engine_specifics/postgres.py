import re
from datetime import datetime
from typing import Any

from engine_specifics.base import BaseSpecificEngine
from sqlalchemy import Date, DateTime, DOUBLE_PRECISION, String, JSON
from sqlalchemy.dialects.postgresql import ENUM

from utils.constants import TimeGrain

from utils.core import GenericDataType

from engine_specifics.base import BasicParametersMixin


class PostgresBaseSpecificEngine(BaseSpecificEngine):
    engine = ""
    engine_name = "PostgreSQL"

    _time_grain_expressions = {
        None: "{col}",
        TimeGrain.SECOND: "DATE_TRUNC('second', {col})",
        TimeGrain.MINUTE: "DATE_TRUNC('minute', {col})",
        TimeGrain.HOUR: "DATE_TRUNC('hour', {col})",
        TimeGrain.DAY: "DATE_TRUNC('day', {col})",
        TimeGrain.WEEK: "DATE_TRUNC('week', {col})",
        TimeGrain.MONTH: "DATE_TRUNC('month', {col})",
        TimeGrain.QUARTER: "DATE_TRUNC('quarter', {col})",
        TimeGrain.YEAR: "DATE_TRUNC('year', {col})",
    }

    @classmethod
    def fetch_data(cls, cursor, limit: int) -> list[tuple[Any, ...]]:
        if not cursor.description:
            return []
        return super().fetch_data(cursor, limit)

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "(timestamp 'epoch' + {col} * interval '1 second')"

    @classmethod
    def convert_dttm(
        cls, target_type: str, dttm: datetime, db_extra: dict[str, Any] | None = None
    ) -> str | None:
        sqla_type = cls.get_sqla_column_type(target_type)

        if isinstance(sqla_type, Date):
            return f"TO_DATE('{dttm.date().isoformat()}', 'YYYY-MM-DD')"
        if isinstance(sqla_type, DateTime):
            dttm_formatted = dttm.isoformat(sep=" ", timespec="microseconds")
            return f"""TO_TIMESTAMP('{dttm_formatted}', 'YYYY-MM-DD HH24:MI:SS.US')"""
        return None


class PostgresSpecificEngine(BasicParametersMixin, PostgresBaseSpecificEngine):
    engine = 'postgresql'
    engine_aliases = {"postgres"}
    supports_dynamic_schema = True

    default_driver = "psycopg2"
    sqlalchemy_uri_placeholder = (
        "postgresql://user:password@host:port/dbname[?key=value&key=value...]"
    )
    encryption_parameters = {"sslmode": "require"}
    max_column_name_length = 63
    try_remove_schema_from_table_name = False

    column_type_mappings = (
        (
            re.compile(r"^double precision", re.IGNORECASE),
            DOUBLE_PRECISION(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^array.*", re.IGNORECASE),
            String(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^json.*", re.IGNORECASE),
            JSON(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^enum.*", re.IGNORECASE),
            ENUM(),
            GenericDataType.STRING,
        ),
    )
