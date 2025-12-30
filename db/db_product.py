
from fastapi import HTTPException,status
from schemas import ProductBase, ProductDisplay
from db.models import DbProduct, DbCategory
from sqlalchemy.orm import Session
from datetime import datetime

def create_product(db: Session, request: ProductBase):
    # Check if the category exists
    category = db.query(DbCategory).filter(DbCategory.category_id == request.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create the product
    new_product = DbProduct(
        product_name=request.product_name,
        price=request.price,
        stock=request.stock,
        image_url=request.image_url,
        category_id=request.category_id,
        created_at=datetime.utcnow()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    # return new_product

    # Attach category object for nested response
    # new_product.category = category
    return new_product

def get_all_products(db:Session):
    return db.query(DbProduct).all()    

def get_product(db:Session,id:int):
    product =  db.query(DbProduct).filter(DbProduct.product_id == id).first() 
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={id} not found"
        )
    return product

def update_product(db: Session, id: int, request: ProductBase):
    product = db.query(DbProduct).filter(DbProduct.product_id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category = db.query(DbCategory).filter(DbCategory.category_id == request.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")    

    product.product_name = request.product_name
    product.price = request.price
    product.stock = request.stock
    product.image_url = request.image_url
    product.category_id = request.category_id

    
    db.commit()
    db.refresh(product)

    
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "created_at": product.created_at,
        "category": {
            "category_id": category.category_id,
            "category_code":category.category_code,
            "category_name":category.category_name
        }
    }
def delete_product(db:Session,id:int):
    product = db.query(DbProduct).filter(DbProduct.product_id == id).first()  
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product with id={id} not found"
        )
    db.delete(product)
    db.commit()
    return 'ok'     



    