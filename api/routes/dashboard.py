from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_user, require_role
from api.deps import get_db, get_current_user
from services.dashboard_service import (
    get_summary,
    category_breakdown,
    recent_activity,
    monthly_trend
)
from schemas.financial_record import FinancialRecordOut

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

ROLES = ["Admin", "Analyst", "Viewer"]  

# Get financial summary
@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    user=Depends(require_role(ROLES))
):
    return get_summary(db, user)

# Get category breakdown
@router.get("/categories")
def categories(
    db: Session = Depends(get_db),
    user=Depends(require_role(ROLES))
):
    return category_breakdown(db, user)

# Get recent activity
@router.get("/recent", response_model=list[FinancialRecordOut])
def recent(
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(require_role(ROLES))
):
    return recent_activity(db, user)

@router.get("/monthly")
def monthly(
    db: Session = Depends(get_db),
    user=Depends(require_role(ROLES))
):
    return monthly_trend(db, user)