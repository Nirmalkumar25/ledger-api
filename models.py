from sqlalchemy import Column, Integer, String, Date, DateTime
from database import Base

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, index=True)
    loan_no = Column(String)
    disbursement_date = Column(Date)
    customer_id = Column(String)
    name = Column(String)
    address = Column(String)
    particulars = Column(String)
    amount = Column(Integer)
    mobile_number = Column(String)



class ColumnVisibility(Base):
    __tablename__ = "column_visibility"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer)
    column_name = Column(String)
