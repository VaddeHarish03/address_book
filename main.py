from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from geopy.distance import geodesic

import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db=db, address=address)

@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses

@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return crud.update_address(db=db, address_id=address_id, address=address)

@app.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return crud.delete_address(db=db, address_id=address_id)

@app.get("/addresses/search/", response_model=List[schemas.Address])
def search_addresses(lat: float, lng: float, distance: float, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db)
    result = []
    for address in addresses:
        if geodesic((lat, lng), (address.latitude, address.longitude)).km <= distance:
            result.append(address)
    return result
