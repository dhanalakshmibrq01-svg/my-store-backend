
from __future__ import annotations
from pydantic import BaseModel,Field
from typing import List
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

class CategoryDisplay(BaseModel):
    category_id: int
    category_code: str
    category_name: str
    class Config():
        orm_mode = True 

class CategoryList(BaseModel):
    categories: List[CategoryDisplay]  

class ProductBase(BaseModel):
    product_name: str
    price: float
    stock: int
    image_url: str
    category_id: int

class ProductDisplay(BaseModel):
    product_id: int
    product_name: str
    price: float
    stock: int
    category: CategoryDisplay 
    image_url: str
    created_at: datetime
    class Config():
        orm_mode = True