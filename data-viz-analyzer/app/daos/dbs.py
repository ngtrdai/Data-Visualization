from daos.base import BaseDAO

from schemas.dbs import DBS


class DbsDAO(BaseDAO[DBS]):
    @staticmethod
    def build_db_for_connection_test(
        server_cert: str,
        extra: str,
        impersonate_user: bool,
        encrypted_extra: str
    ) -> DBS:
        return DBS(
            server_cert=server_cert,
            extra=extra,
            impersonate_user=impersonate_user,
            encrypted_extra=encrypted_extra,
        )
