from datetime import datetime
from re import Pattern, Match
from typing import Union, Callable, Any, TypedDict
import re

from marshmallow import Schema, fields
from marshmallow.validate import Range
from sqlalchemy import types, URL
from sqlalchemy.sql.type_api import TypeEngine

from app.utils.core import GenericDataType, ColumnTypeSource, ColumnSpec, make_url_safe
from app.errors import DataVizError, DataVizErrorType, ErrorLevel
from app.utils.network import is_hostname_valid, is_port_open

ColumnTypeMapping = tuple[
    Pattern[str],
    Union[TypeEngine, Callable[[Match[str]], TypeEngine]],
    GenericDataType,
]


class LimitMethod:
    FETCH_MANY = "fetch_many"
    WRAP_SQL = "wrap_sql"
    FORCE_LIMIT = "force_limit"


class BasicParametersSchema(Schema):
    username = fields.String(
        required=True, allow_none=True, metadata={"description": "Username"}
    )
    password = fields.String(allow_none=True, metadata={"description": "Password"})
    host = fields.String(
        required=True, metadata={"description": "Hostname or IP address"}
    )
    port = fields.Integer(
        required=True,
        metadata={"description": "Database port"},
        validate=Range(min=0, max=2**16, max_inclusive=False),
    )
    database = fields.String(
        required=True, metadata={"description": "Database name"}
    )
    query = fields.Dict(
        keys=fields.Str(),
        values=fields.Raw(),
        metadata={"description": "Additional parameters"},
    )
    encryption = fields.Boolean(
        required=False,
        metadata={"description": "Use an encrypted connection to the database"},
    )
    ssh = fields.Boolean(
        required=False,
        metadata={"description": "Use an ssh tunnel connection to the database"},
    )


class BasicParametersType(TypedDict, total=False):
    username: str | None
    password: str | None
    host: str
    port: int
    database: str
    query: dict[str, Any]
    encryption: bool


class BasicPropertiesType(TypedDict):
    parameters: BasicParametersType


class BasicParametersMixin:
    parameters_schema = BasicParametersSchema()
    default_driver = ""
    encryption_parameters: dict[str, str] = {}

    @classmethod
    def build_sqlalchemy_uri(
        cls,
        parameters: BasicParametersType,
        encrypted_extra: dict[str, str] | None = None,
    ) -> str:
        query = parameters.get("query", {}).copy()
        if parameters.get("encryption"):
            if not cls.encryption_parameters:
                raise Exception(
                    "Unable to build a URL with encryption enabled"
                )
            query.update(cls.encryption_parameters)

        return str(
            URL.create(
                f"{cls.engine}+{cls.default_driver}".rstrip("+"),  # type: ignore
                username=parameters.get("username"),
                password=parameters.get("password"),
                host=parameters["host"],
                port=parameters["port"],
                database=parameters["database"],
                query=query,
            )
        )

    @classmethod
    def get_parameters_from_uri(
        cls, uri: str, encrypted_extra: dict[str, Any] | None = None
    ) -> BasicParametersType:
        url = make_url_safe(uri)
        query = {
            key: value
            for (key, value) in url.query.items()
            if (key, value) not in cls.encryption_parameters.items()
        }
        encryption = all(
            item in url.query.items() for item in cls.encryption_parameters.items()
        )
        return {
            "username": url.username,
            "password": url.password,
            "host": url.host,
            "port": url.port,
            "database": url.database,
            "query": query,
            "encryption": encryption,
        }

    @classmethod
    def validate_parameters(
            cls, properties: BasicPropertiesType
    ) -> list[DataVizError]:
        errors: list[DataVizError] = []

        required = {"host", "port", "username", "database"}
        parameters = properties.get("parameters", {})
        present = {key for key in parameters if parameters.get(key, ())}

        if missing := sorted(required - present):
            errors.append(
                DataVizError(
                    message=f'One or more parameters are missing: {", ".join(missing)}',
                    error_type=DataVizErrorType.CONNECTION_MISSING_PARAMETERS_ERROR,
                    level=ErrorLevel.WARNING,
                    extra={"missing": missing},
                ),
            )

        host = parameters.get("host", None)
        if not host:
            return errors
        if not is_hostname_valid(host):
            errors.append(
                DataVizError(
                    message="The hostname provided can't be resolved.",
                    error_type=DataVizErrorType.CONNECTION_INVALID_HOSTNAME_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["host"]},
                ),
            )
            return errors

        port = parameters.get("port", None)
        if not port:
            return errors
        try:
            port = int(port)
        except (ValueError, TypeError):
            errors.append(
                DataVizError(
                    message="Port must be a valid integer.",
                    error_type=DataVizErrorType.CONNECTION_INVALID_PORT_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["port"]},
                ),
            )
        if not (isinstance(port, int) and 0 <= port < 2 ** 16):
            errors.append(
                DataVizError(
                    message=(
                        "The port must be an integer between 0 and 65535 "
                        "(inclusive)."
                    ),
                    error_type=DataVizErrorType.CONNECTION_INVALID_PORT_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["port"]},
                ),
            )
        elif not is_port_open(host, port):
            errors.append(
                DataVizError(
                    message="The port is closed.",
                    error_type=DataVizErrorType.CONNECTION_PORT_CLOSED_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["port"]},
                ),
            )

        return errors


class BaseSpecificEngine:
    engine_name: str | None = None
    engine: str = "base"
    engine_aliases: set[str] = set()
    drivers: dict[str, str] = {}
    default_driver: str | None = None

    sqlalchemy_uri_placeholder = (
        "engine+driver://user:password@host:port/dbname[?key=value&key=value...]"
    )

    disable_ssh_tunneling = False
    _date_trunc_functions: dict[str, str] = {}
    _time_grain_expressions: dict[str | None, str] = {}
    _default_column_type_mappings: tuple[ColumnTypeMapping, ...] = (
        (
            re.compile(r"^string", re.IGNORECASE),
            types.String(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^n((var)?char|text)", re.IGNORECASE),
            types.UnicodeText(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^(var)?char", re.IGNORECASE),
            types.String(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^(tiny|medium|long)?text", re.IGNORECASE),
            types.String(),
            GenericDataType.STRING,
        ),
        (
            re.compile(r"^smallint", re.IGNORECASE),
            types.SmallInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^int(eger)?", re.IGNORECASE),
            types.Integer(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^bigint", re.IGNORECASE),
            types.BigInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^long", re.IGNORECASE),
            types.Float(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^decimal", re.IGNORECASE),
            types.Numeric(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^numeric", re.IGNORECASE),
            types.Numeric(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^float", re.IGNORECASE),
            types.Float(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^double", re.IGNORECASE),
            types.Float(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^real", re.IGNORECASE),
            types.REAL,
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^smallserial", re.IGNORECASE),
            types.SmallInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^serial", re.IGNORECASE),
            types.Integer(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^bigserial", re.IGNORECASE),
            types.BigInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^money", re.IGNORECASE),
            types.Numeric(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^timestamp", re.IGNORECASE),
            types.TIMESTAMP(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^datetime", re.IGNORECASE),
            types.DateTime(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^date", re.IGNORECASE),
            types.Date(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^time", re.IGNORECASE),
            types.Time(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^interval", re.IGNORECASE),
            types.Interval(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^bool(ean)?", re.IGNORECASE),
            types.Boolean(),
            GenericDataType.BOOLEAN,
        ),
    )

    column_type_mappings: tuple[ColumnTypeMapping, ...] = ()
    column_type_mutators: dict[TypeEngine, Callable[[Any], Any]] = {}

    time_groupby_inline = False
    limit_method = LimitMethod.FORCE_LIMIT
    allows_alias_in_select = True

    arraysize = 0

    custom_errors: dict = {}

    @classmethod
    def get_allows_alias_in_select(cls, database) -> bool:
        return cls.allows_alias_in_select

    @classmethod
    def supports_url(cls, url: URL) -> bool:
        backend = url.get_backend_name()
        driver = url.get_driver_name()
        return cls.supports_backend(backend, driver)

    @classmethod
    def supports_backend(cls, backend: str, driver: str | None = None) -> bool:
        if backend != cls.engine and backend not in cls.engine_aliases:
            return False

        if not cls.drivers or driver is None:
            return True

        return driver in cls.drivers

    @classmethod
    def get_schema_from_engine_params(
            cls,
            sqlalchemy_uri: URL,
            connect_args: dict[str, Any]
    ) -> str | None:
        return None

    @classmethod
    def get_column_types(
        cls,
        column_type: str | None,
    ) -> tuple[TypeEngine, GenericDataType] | None:
        if not column_type:
            return None

        for regex, sqla_type, generic_type in (
                cls.column_type_mappings + cls._default_column_type_mappings
        ):
            match = regex.match(column_type)
            if not match:
                continue
            if callable(sqla_type):
                return sqla_type(match), generic_type
            return sqla_type, generic_type
        return None

    @classmethod
    def get_column_spec(
        cls,
        native_type: str | None,
        db_extra: dict[str, Any] | None = None,
        source: ColumnTypeSource = ColumnTypeSource.GET_TABLE,
    ) -> ColumnSpec | None:
        if col_types := cls.get_column_types(native_type):
            column_type, generic_type = col_types
            is_dttm = generic_type == GenericDataType.TEMPORAL
            return ColumnSpec(
                sqla_type=column_type, generic_type=generic_type, is_dttm=is_dttm
            )
        return None

    @classmethod
    def get_sqla_column_type(
            cls,
            native_type: str | None,
            db_extra: dict[str, Any] | None = None,
            source: ColumnTypeSource = ColumnTypeSource.GET_TABLE,
    ) -> TypeEngine | None:
        column_spec = cls.get_column_spec(
            native_type=native_type,
            db_extra=db_extra,
            source=source,
        )
        return column_spec.sqla_type if column_spec else None

    @classmethod
    def get_datatype(cls, type_code: Any) -> str | None:
        if isinstance(type_code, str) and type_code != "":
            return type_code.upper()
        return None

    @classmethod
    def get_dbapi_exception_mapping(cls) -> dict[type[Exception], type[Exception]]:
        return {}

    @classmethod
    def parse_error_exception(cls, exception: Exception) -> Exception:
        return exception

    @classmethod
    def get_dbapi_mapped_exception(cls, exception: Exception) -> Exception:
        new_exception = cls.get_dbapi_exception_mapping().get(type(exception))
        if not new_exception:
            return cls.parse_error_exception(exception)
        return new_exception(str(exception))

    @classmethod
    def epoch_to_dttm(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def convert_dttm(
        cls, target_type: str, dttm: datetime, db_extra: dict[str, Any] | None = None
    ) -> str | None:
        return

    @classmethod
    def mask_encrypted_extra(cls, encrypted_extra: str | None) -> str | None:
        return encrypted_extra

    @classmethod
    def unmask_encrypted_extra(cls, old: str | None, new: str | None) -> str | None:
        return new

    @classmethod
    def fetch_data(cls, cursor: Any, limit: int | None = None) -> list[tuple[Any, ...]]:
        if cls.arraysize:
            cursor.arraysize = cls.arraysize
        try:
            if cls.limit_method == LimitMethod.FETCH_MANY and limit:
                return cursor.fetchmany(limit)
            data = cursor.fetchall()
            description = cursor.description or []
            column_mutators = {
                row[0]: func
                for row in description
                if (
                    func := cls.column_type_mutators.get(
                        type(cls.get_sqla_column_type(cls.get_datatype(row[1])))
                    )
                )
            }
            if column_mutators:
                indexes = {row[0]: idx for idx, row in enumerate(description)}
                for row_idx, row in enumerate(data):
                    new_row = list(row)
                    for col, func in column_mutators.items():
                        col_idx = indexes[col]
                        new_row[col_idx] = func(row[col_idx])
                    data[row_idx] = tuple(new_row)

            return data
        except Exception as ex:
            raise cls.get_dbapi_mapped_exception(ex) from ex

    @staticmethod
    def mutate_db_for_connection_test(
        database
    ) -> None:
        return None
