from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordOut
)
from services.finance_service import (
    create_record,
    get_records,
    update_record,
    delete_record
)
from api.deps import get_db, get_current_user, require_role
from models.financial_record import FinancialRecord

router = APIRouter(prefix="/finance", tags=["Finance"])


# Create financial record(Admin access only)
@router.post("/", response_model=FinancialRecordOut)
def create_finance(
    data: FinancialRecordCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    return create_record(db, user.id, data)

# Read financial records (Admin can see all, Viewer can see own)
@router.get("/", response_model=list[FinancialRecordOut])
def read_finance(
    record_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin", "Analyst"]))  # 🔥 FIX
):
    filters = {
        "type": record_type,
        "category": category,
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "offset": offset
    }

    return get_records(db, user, filters)


#update financial record (Admin access only)
@router.put("/{record_id}", response_model=FinancialRecordOut)
def update_finance(
    record_id: int,
    data: FinancialRecordUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return update_record(db, record, data)


# Delete financial record (Admin access only)
@router.delete("/{record_id}")
def delete_finance_route(
    record_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != user.id and user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")


    delete_record(db, record)
    return {"message": "Record deleted"}