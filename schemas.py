from pydantic import BaseModel

class AddressBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
