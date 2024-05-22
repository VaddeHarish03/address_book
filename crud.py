from sqlalchemy.orm import Session
import models
import schemas

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Address).offset(skip).limit(limit).all()

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        db_address.name = address.name
        db_address.latitude = address.latitude
        db_address.longitude = address.longitude
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address
