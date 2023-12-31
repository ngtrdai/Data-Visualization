from typing import Dict, Any
from pydantic import BaseModel


class DBSValidateParametersModel(BaseModel):
    id: int = None
    engine: str
    driver: str
    parameters: Dict[str, Any]
    name: str = None
    extra: Dict[str, Any]
