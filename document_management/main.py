from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import schema,utils,models
from database import Base, sessionLOCAL,engine

Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=sessionLOCAL()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")