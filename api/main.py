from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Customer
from repositories import CustomerRepository
from schemas import CustomerRequest, CustomerResponse
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create(request: CustomerRequest, db: Session = Depends(get_db)):
    customer = CustomerRepository.save(db, Customer(**request.dict()))
    return CustomerResponse.from_orm(customer)

@app.get("/customers", response_model=list[CustomerResponse])
def find_all(db: Session = Depends(get_db)):
    customers = CustomerRepository.find_all(db)
    return [CustomerResponse.from_orm(customer) for customer in customers]

@app.get("/customers/{id}", response_model=CustomerResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    customer = CustomerRepository.find_by_id(db, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return CustomerResponse.from_orm(customer)

@app.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not CustomerRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    CustomerRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/customers/{id}", response_model=CustomerResponse)
def update(id: int, request: CustomerRequest, db: Session = Depends(get_db)):
    if not CustomerRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    customer = CustomerRepository.save(db, Customer(id=id, **request.dict()))
    return CustomerResponse.from_orm(customer)
