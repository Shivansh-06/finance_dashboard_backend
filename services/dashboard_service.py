from sqlalchemy.orm import Session
from sqlalchemy import func
from models.financial_record import FinancialRecord

# Get financial summary
def get_summary(db: Session, user):
    total_income = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == "income"
    ).scalar() or 0

    total_expense = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == "expense"
    ).scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }


# Get category breakdown
def category_breakdown(db: Session, user):
    query = db.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label("total")
    ).group_by(FinancialRecord.category)

    return [
        {"category": row[0], "total": row[1]}
        for row in query.all()
    ]
# Get recent activity
def recent_activity(db: Session, user, limit : int =5):
    query = db.query(FinancialRecord).order_by(FinancialRecord.date.desc())

    return query.limit(limit).all()

def monthly_trend(db: Session, user):
    query = db.query(
        func.strftime('%Y-%m', FinancialRecord.date).label("month"),
        FinancialRecord.record_type,
        func.sum(FinancialRecord.amount).label("total")
    ).group_by("month", FinancialRecord.record_type).order_by("month")

    results = {}

    for row in query.all():

        month = row[0]

        if month not in results:

            results[month] = {"month": month, "income": 0, "expense": 0}

        results[month][row[1]] = row[2]


    return list(results.values())