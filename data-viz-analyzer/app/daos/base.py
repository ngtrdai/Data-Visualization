from typing import Generic, TypeVar, get_args

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseDAO(Generic[T]):
    __orig_bases__ = None
    id_column_name = "id"

    model_cls: type[BaseModel] | None = None

    def __init_subclass__(cls) -> None:
        cls.model_cls = get_args(cls.__orig_bases__[0])[0]

    @classmethod
    def get_model(cls) -> type[BaseModel]:
        return cls.model_cls

    @classmethod
    def find_by_id(
        cls,
        model_id: str | int,
        session: Session
    ) -> T | None:
        query = session.query(cls.model_cls)
        column_id = getattr(cls.model_cls, cls.id_column_name)
        try:
            return query.filter(column_id == model_id).one_or_none()
        except StatementError:
            return None
