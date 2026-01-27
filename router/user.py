
from typing import List
from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from schemas import UserBase,UserDisplay
from db.database import get_db
from db import db_user

from auth.token_utils import oauth2_schema,get_current_user
# from auth.token_utils import get_current_user

router = APIRouter(
     prefix='/user',
     tags=['user']
)


# @router.post("/",response_model=UserDisplay)
# def create_user(request:UserBase,db:Session = Depends(get_db)):
#     return db_user.create_user(db,request)

@router.get("/",response_model=List[UserDisplay])
def get_all_users(db:Session = Depends(get_db),current_user:UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)

@router.get("/{id}",response_model=UserDisplay)  
def get_user(id:int,db:Session=Depends(get_db),current_user:UserBase = Depends(get_current_user)):
    return db_user.get_user(db,id)   

# @router.get("/{username}", response_model=UserDisplay)
# def get_user(username: str, db: Session = Depends(get_db),current_user:UserBase = Depends(get_current_user)):
#     return db_user.get_user_by_username(db, username)
    
    

# @router.post("/{id}/update",response_model=UserDisplay)
# def update_user(id:int,request:UserBase, db:Session = Depends(get_db),current_user:UserBase = Depends(get_current_user)):
#    return db_user.update_user(db,id,request)   

# @router.get("/delete/{id}")
# def delete_user(user_id:int,db:Session = Depends(get_db),current_user:UserBase = Depends(get_current_user)):
#     return db_user.delete_user(db,user_id)   


