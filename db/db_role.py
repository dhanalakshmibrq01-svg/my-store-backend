

from schemas import RoleBase
from db.models import DbRole
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

def create_role(db: Session, request: RoleBase):
    new_role = DbRole(
        role_code=request.role_code,
        role_name = request.role_name
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def get_all_roles(db:Session):
    return db.query(DbRole).all() 

def get_role(db:Session,id:int):
    role = db.query(DbRole).filter(DbRole.role_id == id).first() 
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id={id} not found"
        )
    return role

def update_role(db: Session, id: int, request: RoleBase):
    role = db.query(DbRole).filter(DbRole.role_id == id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Role with id={id} not found"
        )
    role.role_code = request.role_code
    role.role_name = request.role_name

    db.commit()
    db.refresh(role)

    return {
        "role_id": role.role_id,
        "role_code": role.role_code,
        "role_name": role.role_name
    }

def delete_role(db:Session,id:int):
    role = db.query(DbRole).filter(DbRole.role_id == id).first()  
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Role with id={id} not found"
        )
    db.delete(role)
    db.commit()
    return 'ok' 


