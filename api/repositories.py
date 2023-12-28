from sqlalchemy.orm import Session

from models import Customer

class CustomerRepository:
    
    @staticmethod
    def find_all(db: Session) -> list[Customer]:
        return db.query(Customer).all()

    @staticmethod
    def save(db: Session, customer: Customer) -> Customer:
        if customer.id:
            db.merge(customer)
        else:
            db.add(customer)
        db.commit()
        return customer

    @staticmethod
    def find_by_id(db: Session, id: int) -> Customer:
        return db.query(Customer).filter(Customer.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Customer).filter(Customer.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        customer = db.query(Customer).filter(Customer.id == id).first()
        if customer is not None:
            db.delete(customer)
            db.commit()
