from sqlalchemy.orm import Session
from models.financial_record import FinancialRecord
from datetime import datetime


def create_record(db: Session, user_id: int, data):
    record = FinancialRecord(
        user_id=user_id,
        amount=data.amount,
        record_type=data.record_type,
        category=data.category,
        description=data.description,
        date=data.date if hasattr(data, "date") and data.date else datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_records(db: Session, user, filters: dict):
    query = db.query(FinancialRecord)

    if filters.get("type"):
        query = query.filter(FinancialRecord.record_type == filters["type"])

    if filters.get("category"):
        query = query.filter(FinancialRecord.category == filters["category"])

    if filters.get("start_date"):
        query = query.filter(FinancialRecord.date >= filters["start_date"])

    if filters.get("end_date"):
        query = query.filter(FinancialRecord.date <= filters["end_date"])

    # pagination
    return query.offset(filters.get("offset", 0)).limit(filters.get("limit", 10)).all()


def update_record(db: Session, record: FinancialRecord, data):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record: FinancialRecord):
    db.delete(record)
    db.commit()