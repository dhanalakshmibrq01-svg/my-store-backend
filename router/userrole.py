
from schemas import UserRoleBase,UserRoleDisplay,UserRoleResponse
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import user_role
from typing import List
from schemas import UserBase
from auth.token_utils import get_current_user

router=APIRouter(
    prefix='/user-role',
    tags=['roles']
)

@router.post("/", response_model=UserRoleDisplay)
def assign_role(request: UserRoleBase, db: Session = Depends(get_db)):
    return user_role.assign_role(db, request)

@router.get("/", response_model=List[UserRoleDisplay])
def get_all_user_roles(db: Session = Depends(get_db)):
    return user_role.get_all_user_roles(db)

# @router.get("/{user_id}",response_model=List[UserRoleDisplay])  
@router.get("/{user_id}",response_model=UserRoleResponse)
def  get_user_roles(user_id:int,db: Session = Depends(get_db),current_user:UserBase = Depends(get_current_user)):
    return {
        'data':user_role.get_user_roles(db,user_id),
        'current_user':current_user
    } 

