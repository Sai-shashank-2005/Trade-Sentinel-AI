from sqlalchemy import Column, Integer, String
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer)
    risk_level = Column(String)
