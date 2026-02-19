import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Transaction

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...), db: Session = Depends(get_db)):

    df = pd.read_csv(file.file)

    for _, row in df.iterrows():
        txn = Transaction(
            transaction_id=int(row["transaction_id"]),
            risk_level="Not Processed"
        )
        db.add(txn)

    db.commit()

    return {
        "message": "File processed successfully",
        "records_inserted": len(df)
    }
