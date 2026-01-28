
from fastapi import HTTPException,status
from schemas import ProductBase, ProductDisplay
from db.models import DbProduct, DbCategory
from sqlalchemy.orm import Session
from datetime import datetime

def create_product(db: Session, request: ProductBase):
    fields = {
        "Product name": request.product_name,
        "Description": request.description,
        "Image URL": request.image_url
    }

    for field_name, value in fields.items():
        if not value or not value.strip() or value.strip().lower() == "string":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field_name} cannot be empty or default value"
            )

    if request.price is None or request.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0"
        )

    if request.stock is None or request.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative"
        )

    if not request.category_id or request.category_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category is required"
        )
        
    category = db.query(DbCategory).filter(DbCategory.category_id == request.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if db.query(DbProduct).filter(
        DbProduct.product_name.ilike(request.product_name.strip())).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exists"
    )
    
    new_product = DbProduct(
        product_name=request.product_name,
        description=request.description,
        price=request.price,
        stock=request.stock,
        image_url=request.image_url,
        category_id=request.category_id,
        created_at=datetime.utcnow()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
   
    return new_product


# def search_product_by_name(db: Session, keyword: str):
#     keyword = keyword.strip()
#     if not keyword:
#         return []

    
#     starts_with = db.query(DbProduct).filter(
#         DbProduct.product_name.ilike(f"{keyword}%")
#     ).all()

    
#     contains = db.query(DbProduct).filter(
#         DbProduct.product_name.ilike(f"%{keyword}%"),
#         ~DbProduct.product_name.ilike(f"{keyword}%")  
#     ).all()

    
#     return starts_with + contains
   

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
    product.description = request.description
    product.price = request.price
    product.stock = request.stock
    product.image_url = request.image_url
    product.category_id = request.category_id

    
    db.commit()
    db.refresh(product)

    
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "description":product.description,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "created_at": product.created_at,
        "category": {
            "category_id": category.category_id,
            
            "category_name":category.category_name,
            "image_url":category.image_url
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

# def get_products_by_category(db: Session, category_id: int):
#     category = db.query(DbCategory).filter(DbCategory.category_id == category_id).first()
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return db.query(DbProduct).filter(DbProduct.category_id == category_id).all()



def search_product(db: Session, keyword: str = "", category_id: int = None):
    keyword = (keyword or "").strip()
    query = db.query(DbProduct)

    if category_id:
        query = query.filter(DbProduct.category_id == category_id)

    if keyword:
        
        starts_with = query.filter(DbProduct.product_name.ilike(f"{keyword}%")).all()
        contains = query.filter(
            DbProduct.product_name.ilike(f"%{keyword}%"),
            ~DbProduct.product_name.ilike(f"{keyword}%")
        ).all()
        result = starts_with + contains
    else:
        result = query.all()

    
    if not result:
        raise HTTPException(status_code=404, detail="No products found for this category and keyword")

    return result



    