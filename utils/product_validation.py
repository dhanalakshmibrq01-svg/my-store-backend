
# utils/product_validation.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import DbProduct, DbCategory
from utils.string_utils import normalize_string

def validate_product(db: Session, request, product_id: int = None):
    # Validate text fields
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

    # Validate price
    if request.price is None or request.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0"
        )

    # Validate stock
    if request.stock is None or request.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative"
        )

    # Validate category
    if not request.category_id or request.category_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category is required"
        )

    category = db.query(DbCategory).filter(
        DbCategory.category_id == request.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check duplicate product name ignoring spaces and case
    # normalized_input_name = normalize_string(request.product_name)
    # existing_products = db.query(DbProduct).all()

    # for product in existing_products:
    #     if product_id and product.product_id == product_id:
    #         continue
    #     if normalize_string(product.product_name) == normalized_input_name:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Product name already exists"
    #         )
    normalized_name = normalize_string(request.product_name)
    existing_products = db.query(DbProduct).all()
    for product in existing_products:
        if product_id and product.product_id == product_id:
            continue

        if normalize_string(product.product_name) == normalized_name:
           raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exists"
        )