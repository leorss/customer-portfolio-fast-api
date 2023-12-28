from pydantic import BaseModel

class CustomerBase(BaseModel):
    cnpj: str
    name: str
    longitude: str
    latitude: str

class CustomerRequest(CustomerBase):
    ...

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True
