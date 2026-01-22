

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
    employees = relationship("DbEmployee", back_populates="department")
    
class DbRole(Base):
    __tablename__='role' 
    role_id = Column(Integer,primary_key=True,index=True)
    role_code = Column(String)
    role_name = Column(String)
    employees = relationship("DbEmployee", back_populates="role")

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

class SystemRole(Base):
    __tablename__ = "system_role"

    sr_id = Column(Integer, primary_key=True)       
    sr_name = Column(String(50), nullable=False, unique=True)

    
    # users = relationship("DbUser", back_populates="role")
    user_roles = relationship("UserRole", back_populates="role")

class DbUser(Base):
    __tablename__ = 'login'    
    user_id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    password = Column(String)
    sr_id = Column(Integer, nullable=False)
    # sr_id = Column(Integer, ForeignKey("system_role.sr_id"))
    is_active = Column(String(3), default="YES")

    # role = relationship("SystemRole", back_populates="users")
    # roles = relationship("UserRole", back_populates="user")
    employees = relationship("DbEmployee", back_populates="user")
    

# class SystemRole(Base):
#     __tablename__ = "system_role"
#     sr_id = Column(Integer, primary_key=True)        
#     sr_name = Column(String(50),nullable=False, unique=True)

#     users = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "user_role"

    user_role_id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("login.user_id"), nullable=False)  
    sr_id = Column(Integer, ForeignKey("system_role.sr_id"), nullable=False) 
    created_on = Column(DateTime, default=datetime.utcnow) 
    
    # user = relationship("DbUser", back_populates="roles")      
    role = relationship("SystemRole", back_populates="user_roles")    


class DbEmployee(Base):
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("login.user_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)

   
    user = relationship("DbUser",back_populates="employees")
    role = relationship("DbRole",back_populates="employees")
    department = relationship("DbDepartment",back_populates="employees")