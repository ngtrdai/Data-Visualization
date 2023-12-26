import builtins
import inspect
import textwrap
import uuid
import json
from marshmallow import EXCLUDE, fields, pre_load, Schema, validates_schema, ValidationError
from marshmallow.validate import Length
from sqlalchemy import Column, Integer, Uuid, String, MetaData, Boolean, Text, URL
from sqlalchemy.exc import NoSuchModuleError

from utils.constants import PASSWORD_MASK
from utils.core import make_url_safe

from engine_specifics import get_engine_specific
from engine_specifics.base import BaseSpecificEngine
from database import Base
from schemas.base_entity import BaseEntity


def extra_validator(value: str) -> str:
    if value:
        try:
            extra_ = json.loads(value)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Field cannot be decoded by JSON. {str(e)}") from e

        metadata_signature = inspect.signature(MetaData)
        for key in extra_.get('metadata_params', {}):
            if key not in metadata_signature.parameters:
                raise ValidationError(f"Invalid metadata parameter {key}")

    return value


class DBS(Base, BaseEntity):
    __tablename__ = "dbs"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(Uuid, unique=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    sqlalchemy_uri = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    encrypted_extra = Column(String, nullable=True)
    server_cert = Column(String, nullable=True)
    impersonate_user = Column(Boolean, default=False)
    extra = Column(
        Text,
        default=textwrap.dedent(
            """
            {
                "metadata_params": {},
                "engine_params": {},
                "metadata_cache_timeout": {},
                "schemas_allowed_for_file_upload": []
            }
            """
        )
    )

    def set_sqlalchemy_uri(self, uri: str) -> None:
        conn = make_url_safe(uri.strip())
        if conn.password != PASSWORD_MASK:
            self.password = conn.password
        conn = conn.set(password=PASSWORD_MASK if conn.password else None)
        self.sqlalchemy_uri = str(conn)

    @property
    def sqlalchemy_uri_decrypted(self) -> str:
        try:
            conn = make_url_safe(self.sqlalchemy_uri)
        except ValueError:
            return "dialect://invalid_uri"
        conn = conn.set(password=self.password)
        return str(conn)

    @property
    def db_engine_specific(self) -> builtins.type[BaseSpecificEngine]:
        url = make_url_safe(self.sqlalchemy_uri_decrypted)
        return self.get_db_engine_specific(url)

    @classmethod
    def get_db_engine_specific(
        cls, url: URL
    ) -> builtins.type[BaseSpecificEngine]:
        backend = url.get_backend_name()
        try:
            driver = url.get_driver_name()
        except NoSuchModuleError:
            driver = None

        return get_engine_specific(backend, driver)

    class Config:
        orm_mode = True


class DBSValidateParametersSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(
        allow_none=True,
        metadata={
            "description": "The ID of the database connection",
            "example": 1
        }
    )
    engine = fields.String(
        required=True,
        metadata={
            "description": "SQLAlchemy engine to use",
            "example": "postgresql"
        }
    )
    driver = fields.String(
        required=True,
        metadata={
            "description": "SQLAlchemy driver to use",
            "example": "psycopg2"
        }
    )
    parameters = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(allow_none=True),
        metadata={"description": "DB-specific parameters for configuration"}
    )
    name = fields.String(
        metadata={"description": "The name of the database connection"},
        allow_none=True,
        validate=Length(1, 250)
    )
    extra = fields.Dict(
        metadata={"description": "Extra parameters"},
        keys=fields.String(),
        values=fields.Raw(allow_none=True),
        validate=extra_validator
    )
