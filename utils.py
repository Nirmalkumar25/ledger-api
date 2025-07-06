from sqlalchemy.orm import Session
from models import ColumnVisibility

def get_allowed_columns(db: Session, entity_id: int):
    cols = db.query(ColumnVisibility.column_name).filter_by(entity_id=entity_id).all()
    return [col[0] for col in cols]
