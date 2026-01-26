

from schemas import ProductBase,ProductDisplay,ProductByCategory,CategoryDisplay
from fastapi import APIRouter,Depends,HTTPException,status,Request,Query
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_product
from db.models import DbProduct
from typing import Optional
# from models.db_product import DbCategory
from typing import List

router=APIRouter(
    prefix='/product',
    tags=['product']
)

#create product

@router.post('/',response_model=ProductDisplay)
def create_product(request : ProductBase,db:Session = Depends(get_db)):
    return db_product.create_product(db,request)

# @router.get("/search", response_model=List[ProductDisplay])
# def search_products(keyword: str, db: Session = Depends(get_db)):
#     return db_product.search_product_by_name(db, keyword)    



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


# @router.get("/category/{category_id}", response_model=List[ProductDisplay])
# def get_products_by_category(category_id: int, db: Session = Depends(get_db)):

   
#     products = db.query(DbProduct).filter(DbProduct.category_id == category_id).all()

#     if not products:
#         raise HTTPException(status_code=404, detail="No products found for this category")

    
#     return [
#         ProductDisplay(
#             product_id=p.product_id,
#             product_name=p.product_name,
#             description=p.description,
#             price=p.price,
#             stock=p.stock,
#             image_url=p.image_url,
#             created_at=p.created_at,
#             category=CategoryDisplay(  
#                 category_id=p.category.category_id,
#                 category_code=p.category.category_code,
#                 category_name=p.category.category_name,
#                 image_url=p.category.image_url
#             )
#         )
#         for p in products
#     ]
@router.get("/product/", response_model=List[ProductDisplay])
def get_product_by_category(
    keyword: Optional[str] = Query(None, description="Search term"),
    category: Optional[int] = Query(None, description="Category ID to filter"),
    db: Session = Depends(get_db)):
    return db_product.search_product(db, keyword or "", category)
