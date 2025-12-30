

from schemas import ProductBase,ProductDisplay
from fastapi import APIRouter,Depends,HTTPException,status,Request
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_product
from typing import List

router=APIRouter(
    prefix='/product',
    tags=['product']
)

#create product

@router.post('/',response_model=ProductDisplay)
def create_product(request : ProductBase,db:Session = Depends(get_db)):
    return db_product.create_product(db,request)

#get all products
# @router.get('/',response_model=ProductDisplay)
# def get_all_products(db:Session = Depends(get_db)):
#     return db_product.get_all_products(db)

@router.get("/", response_model=List[ProductDisplay])
def get_all_products(request:Request,db: Session = Depends(get_db)):
    products = db_product.get_all_products(db)  
    for p in products:
       if not p.image_url.startswith("http"): 
          p.image_url = str(request.base_url) + f"media/products/{p.image_url}"
    return products

@router.get('/{id}',response_model=ProductDisplay)   
def get_product(id:int,db:Session = Depends(get_db)):
    return db_product.get_product(db,id)       
  
@router.post("/{id}/update",response_model=ProductDisplay)
def update_product(id:int,request:ProductBase,db:Session = Depends(get_db)):
    return db_product.update_product(db,id,request)   

@router.get("/{id}/delete")
def delete_product(id:int,db:Session = Depends(get_db)):
    return db_product.delete_product(db,id)    
