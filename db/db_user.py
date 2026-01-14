
from fastapi import HTTPException,status
from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db import models

def create_user(db:Session,request:UserBase):
    new_user = DbUser(
        username = request.username,
        password = Hash.bcrypt(request.password),
        is_active="NO"  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db:Session):
    return db.query(DbUser).all()    

def get_user(db:Session,id:int):
    user=db.query(DbUser).filter(DbUser.user_id==id).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    return user  

def get_user_by_username(db:Session,username:str):
    user=db.query(DbUser).filter(DbUser.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {username} not found")
    return user      

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.user_id == id).first()  
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with {id} not found"
        )

    
    user.username = request.username
    user.password = Hash.bcrypt(request.password)


    db.commit()
    db.refresh(user) 
    return user 

# def delete_user(db:Session,id:int):
#     user=db.query(DbUser).filter(DbUser.user_id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
      
#     db.delete(user)
#     db.commit()
#     return 'ok'    

def delete_user(db: Session, user_id: int):
    
    db.query(models.UserRole).filter(models.UserRole.user_id == user_id).delete()
    
    
    deleted = db.query(models.DbUser).filter(models.DbUser.user_id == user_id).delete()
    
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}

# def set_active_user(db: Session, user_id: int):
    
#     db.query(DbUser).update({"is_active": "NO"})

    
#     db.query(DbUser)\
#         .filter(DbUser.user_id == user_id)\
#         .update({"is_active": "YES"})

    
#     db.commit()    

