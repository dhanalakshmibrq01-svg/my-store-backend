
from schemas import CategoryBase
from db.models import DbCategory
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

def create_category(db: Session, request: CategoryBase):
    new_category = DbCategory(
        category_code=request.category_code,
        category_name = request.category_name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_all_categories(db:Session):
    return db.query(DbCategory).all()     

def get_category(db:Session,id:int):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first() 
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id={id} not found"
        )
    return category


def update_category(db: Session, id: int, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id={id} not found"
        )
    category.category_code = request.category_code
    category.category_name = request.category_name

    db.commit()
    db.refresh(category)

    return {
        "category_id": category.category_id,
        "category_code": category.category_code,
        "category_name": category.category_name
    }

def delete_category(db:Session,id:int):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first()  
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id={id} not found"
        )
    db.delete(category)
    db.commit()
    return 'ok' 