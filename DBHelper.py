from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    Integer,
    Float,
    String,
    and_,
    func,
    Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import declarative_base

connection_string = "sqlite:///test_db.db"
engine = create_engine(connection_string, echo=True)
Base = declarative_base()
    
class Client(Base):
    __tablename__ = "Client"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)

    orders = relationship("Order", back_populates="client")
    employees = relationship("Employee", secondary="ClientEmployee", back_populates="clients")

    def to_json(self):
        return {"user_id" : self.user_id, 
                "username": self.username,
                "email": self.email}
    
class Order(Base):
    __tablename__ = "Order"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("Client.user_id"))
    description = Column(String)

    client = relationship("Client", back_populates="orders")

    def to_json(self):
        return {
            "order_id": self.order_id,
            "client_id": self.client_id,
            "description": self.description
        }

class Employee(Base):
    __tablename__ = "Employee"
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String)
    post = Column(String)
    salary = Column(Float)
    start_date = Column(String)

    clients = relationship("Client", secondary="ClientEmployee", back_populates="employees")

    def to_json(self):
        return {
            "employee_id": self.employee_id,
            "employee_name": self.employee_name,
            "post": self.post,
            "salary": self.salary,
            "start_date": self.start_date
        }

ClientEmployee = Table('ClientEmployee', Base.metadata,
    Column('client_id', Integer, ForeignKey('Client.user_id'), primary_key=True),
    Column('employee_id', Integer, ForeignKey('Employee.employee_id'), primary_key=True)
)

