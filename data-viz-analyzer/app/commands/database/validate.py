import json
from typing import Any, Optional

from commands.base import BaseCommand
from engine_specifics import get_engine_specific
from daos.dbs import DbsDAO

BYPASS_VALIDATION = []


class ValidateDatabaseParametersCommand(BaseCommand):
    def __init__(self, properties: dict[str, Any], db_context: Optional[Any] = None):
        self._properties = properties.copy()
        self._model = None
        self._db_context = db_context

    def validate(self) -> None:
        if (database_id := self._properties.get("id")) is not None:
            self._model = DbsDAO.find_by_id(database_id, self._db_context)

    def run(self) -> None:
        self.validate()

        engine = self._properties.get('engine')
        driver = self._properties.get('driver')

        if engine in BYPASS_VALIDATION:
            return

        engine_specific = get_engine_specific(engine, driver)

        if not hasattr(engine_specific, "parameters_schema"):
            raise NotImplementedError(
                f"Engine {engine} does not have a parameters schema"
            )

        errors = engine_specific.validate_parameters(self._properties)
        if errors:
            raise ValueError(errors)

        serialized_encrypted_extra = self._properties.get(
            "masked_encrypted_extra",
            "{}",
        )

        if self._model:
            serialized_encrypted_extra = engine_specific.unmask_encrypted_extra(
                self._model.encrypted_extra,
                serialized_encrypted_extra,
            )
        try:
            encrypted_extra = json.loads(serialized_encrypted_extra)
        except json.decoder.JSONDecodeError:
            encrypted_extra = {}

        sqlalchemy_uri = engine_specific.build_sqlalchemy_uri(
            self._properties.get("parameters"),
            encrypted_extra
        )

        if self._model and sqlalchemy_uri == self._model.safe_sqlalchemy_uri():
            sqlalchemy_uri = self._model.sqlalchemy_uri_decrypted

        database = DbsDAO.build_db_for_connection_test(
            server_cert=self._properties.get("server_cert", ""),
            extra=self._properties.get("extra", "{}"),
            impersonate_user=self._properties.get("impersonate_user", False),
            encrypted_extra=serialized_encrypted_extra,
        )

        database.set_sqlalchemy_uri(sqlalchemy_uri)
        database.db_engine_specific.mutate_db_for_connection_test(database)
