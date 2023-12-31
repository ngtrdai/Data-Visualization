import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from schemas.dbs import DBS
from models.dbs import DBSValidateParametersModel
from schemas.dbs import DBSValidateParametersSchema
from commands.database.validate import ValidateDatabaseParametersCommand
from database import get_db_context

router = APIRouter(prefix='/database', tags=['Database'])


def http_exception():
    return HTTPException(status_code=404, detail="Item not found")


@router.get("")
async def get_database_connections(db: Session = Depends(get_db_context)):
    return {
        "message": "OK",
        "data": db.query(DBS).all()
    }


@router.post("")
async def connect_to_database(db: Session = Depends(get_db_context)) -> dict:
    return {"message": "OK"}


@router.post("/check", status_code=status.HTTP_200_OK)
async def check_connection(request: DBSValidateParametersModel, db: Session = Depends(get_db_context)) -> dict:
    try:
        payload = DBSValidateParametersSchema().load(json.loads(request.json()))
    except ValidationError as e:
        errors = []
        raise HTTPException(status_code=400, detail=errors) from e

    command = ValidateDatabaseParametersCommand(payload, db)
    command.run()

    return {"message": "OK"}
