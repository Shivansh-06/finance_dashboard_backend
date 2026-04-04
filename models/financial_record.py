from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(Float, nullable=False)
    record_type = Column(String, nullable=False)  # income / expense
    category = Column(String, nullable=True)

    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=True)

    user = relationship("User")