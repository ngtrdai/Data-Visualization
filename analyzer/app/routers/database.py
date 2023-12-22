from fastapi import APIRouter
from database import LocalSession

router = APIRouter(prefix='/database', tags=['Database'])


def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()


@router.post("")
async def connect_to_database() -> dict:
    return {"message": "OK"}


@router.post("/check")
async def check_connection() -> dict:
    return {"message": "OK"}
