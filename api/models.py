from typing import Optional
from sqlmodel import Field, SQLModel

class Customer(SQLModel, table=True):
    __tablename__ = "customer"
    id: Optional[int] = Field(default=None, primary_key=True)
    cnpj: str
    name: str
    longitude: str
    latitude: str
