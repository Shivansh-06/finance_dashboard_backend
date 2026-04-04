from pydantic import BaseModel, ConfigDict
from typing import Optional

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)