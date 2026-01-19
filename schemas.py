
from __future__ import annotations
from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime 

class DepartmentBase(BaseModel):
    #id:int
    code:str
    name:str

class DepartmentDisplay(BaseModel):
    id: int
    code: str
    name: str
    class Config():
        orm_mode = True

class DepartmentList(BaseModel):
    departments: List[DepartmentDisplay]

class RoleBase(BaseModel):
    role_code:str
    role_name:str    

class RoleDisplay(BaseModel):
    role_id: int
    role_code: str
    role_name: str
    class Config():
        orm_mode = True

class RoleList(BaseModel):
    roles: List[RoleDisplay]    

class CategoryBase(BaseModel):
    category_code : str
    category_name : str   
    image_url: str

class CategoryDisplay(BaseModel):
    category_id: int
    category_code: str
    category_name: str
    image_url: str
    class Config():
        orm_mode = True 

class CategoryList(BaseModel):
    categories: List[CategoryDisplay]  

class ProductBase(BaseModel):
    product_name: str
    description : str
    price: float
    stock: int
    image_url: str
    category_id: int

class ProductDisplay(BaseModel):
    product_id: int
    product_name: str
    description: str
    price: float
    stock: int
    category: CategoryDisplay 
    image_url: str
    created_at: datetime
    class Config():
        orm_mode = True

class ProductByCategory(BaseModel):
    product_id: int
    product_name: str
    description: str
    price: float
    stock: int
    image_url: str
    created_at: datetime
    # category_id: Optional[int]  

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username : str
    password : str    
    

class UserDisplay(BaseModel):
    user_id: int
    username: str
    is_active: str
    class Config:
        orm_mode = True

class SystemRoleDisplay(BaseModel):
    sr_id: int
    sr_name: str
    class Config:
        orm_mode = True  

class UserRoleBase(BaseModel):
    user_id: int
    sr_id: int


class UserRoleDisplay(BaseModel):
    user_role_id: int
    user: UserDisplay  
    role: SystemRoleDisplay 
    
    created_on: datetime

    class Config:
        orm_mode = True

class UserRoleResponse(BaseModel):
    data: List[UserRoleDisplay]
    current_user: UserBase

class EmployeeBase(BaseModel):
    name: str
    phone_no: str
    user_id: int
    role_id: int
    department_id: int

class EmployeeDisplay(BaseModel):
    emp_id: int
    name: str
    phone_no: str
    user: UserDisplay
    role: RoleDisplay
    department: DepartmentDisplay

    class Config:
        orm_mode = True

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[str] = None        
