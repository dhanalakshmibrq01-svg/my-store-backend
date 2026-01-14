
from schemas import UserRoleBase
from db.models import UserRole
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException,status,Request

def assign_role(db: Session, request: UserRoleBase):

    
    existing = db.query(UserRole).filter(
        UserRole.user_id == request.user_id,
        UserRole.sr_id == request.sr_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This role is already assigned to this user"
        )

    new_user_role = UserRole(
        user_id=request.user_id,
        sr_id=request.sr_id
    )

    db.add(new_user_role)
    db.commit()
    db.refresh(new_user_role)

    # return new_user_role
    user_role_with_rel = db.query(UserRole).options(
    joinedload(UserRole.user),
    joinedload(UserRole.role)
).filter(UserRole.user_role_id == new_user_role.user_role_id).first()


    return user_role_with_rel

def get_all_user_roles(db: Session):
    
    user_roles = db.query(UserRole).options(
        joinedload(UserRole.user),
        joinedload(UserRole.role)
    ).all()
    return user_roles

def get_user_roles(db: Session, user_id: int):
    user_roles = db.query(UserRole).options(
        joinedload(UserRole.user),  
        joinedload(UserRole.role) 
    ).filter(UserRole.user_id == user_id).all()  
    
    return user_roles  

