from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from schemas.database import CheckConnectionSchema
from database import get_db_context

router = APIRouter(prefix='/database', tags=['Database'])


@router.post("")
async def connect_to_database(db: Session = Depends(get_db_context)) -> dict:
    return {"message": "OK"}


@router.post("/check", status_code=status.HTTP_200_OK)
async def check_connection(request: CheckConnectionSchema) -> dict:
    return {"message": "OK"}
