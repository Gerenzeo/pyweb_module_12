from datetime import date

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.db.db import get_db
from src.routes import contacts, auth

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hi! I am FastAPI applicataion!"}

@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database configured is not correctly!")
        return {"message": "Database correctly working!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    


app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")