from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resource Vault API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://resource-vault-api.netlify.app/"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/resources/", response_model=schemas.Resource)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    db_resource = models.Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.get("/resources/", response_model=List[schemas.Resource])
def read_resources(skip: int = 0, limit: int = 100, search: str = "", db: Session = Depends(get_db)):
    query = db.query(models.Resource)
    if search:
        query = query.filter(
            models.Resource.title.contains(search) |
            models.Resource.tags.contains(search)
        )
    return query.offset(skip).limit(limit).all()

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(db_resource)
    db.commit()
    return {"message": "Deleted"}

@app.get("/")
def root():
    return {"message": "Resource Vault API v1"}