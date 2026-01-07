

from sqlalchemy import Integer,String,Column,Float,DateTime,ForeignKey
from datetime import datetime
#from sqlalchemy.sql.schema import ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class DbDepartment(Base):
    __tablename__='department'
    id = Column(Integer,primary_key=True,index=True)
    code = Column(String)
    name = Column(String)

class DbRole(Base):
    __tablename__='role' 
    role_id = Column(Integer,primary_key=True,index=True)
    role_code = Column(String)
    role_name = Column(String)

class DbCategory(Base):
    __tablename__ = 'category'
    category_id = Column(Integer,primary_key=True,index=True)
    category_code = Column(String)
    category_name = Column(String)
    image_url = Column(String, nullable=True)
    products = relationship("DbProduct", back_populates="category")

class DbProduct(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float)  
    stock = Column(Integer)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    
    category_id = Column(Integer, ForeignKey("category.category_id"))
    category = relationship("DbCategory", back_populates="products")

#class DbEmployee(Base):
    #__tablename__='employees'
    #emp_id=Column(Integer,primary_key=True,index=True)
    #fullname=Column(String)
    #email=Column(String)
    #dept_id=Column(Integer,ForeignKey('departments.dept_id'))

