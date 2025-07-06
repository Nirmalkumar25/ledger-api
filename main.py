from fastapi import FastAPI, Depends, Request, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, LedgerEntry
from rate_limiter import rate_limiter
from utils import get_allowed_columns

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ledger Report Search API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search/")
def search_ledger(
    request: Request,
    entity_id: int,
    name: str = Query(None),
    mobile_number: str = Query(None),
    customer_id: str = Query(None),
    area: str = Query(None),
    db: Session = Depends(get_db),
):
    rate_limiter(request)

    query = db.query(LedgerEntry).filter(LedgerEntry.entity_id == entity_id)

    if name:
        query = query.filter(LedgerEntry.name.ilike(f"%{name}%"))
    if mobile_number:
        query = query.filter(LedgerEntry.mobile_number.ilike(f"%{mobile_number}%"))
    if customer_id:
        query = query.filter(LedgerEntry.customer_id.ilike(f"%{customer_id}%"))
    if area:
        query = query.filter(LedgerEntry.address.ilike(f"%{area}%"))

    allowed_columns = get_allowed_columns(db, entity_id)
    result = query.all()

    def filtered_row(entry):
        return {col: getattr(entry, col) for col in allowed_columns if hasattr(entry, col)}
    
    return [filtered_row(entry) for entry in result]
