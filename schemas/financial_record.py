from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime

# Create record
class FinancialRecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    record_type: Literal["income", "expense"]
    category: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)


# Update financial record
class FinancialRecordUpdate(BaseModel):
    amount: Optional[float] = None
    record_type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    description: Optional[str] = None


# Output financial record schema
class FinancialRecordOut(BaseModel):
    id: int
    user_id: int
    amount: float
    record_type: str
    category: Optional[str]
    description: Optional[str]
    date: datetime

    model_config = ConfigDict(from_attributes=True)
