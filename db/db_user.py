
from fastapi import HTTPException,status
from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser

def create_user(db:Session,request:UserBase):
    new_user = DbUser(
        username = request.username,
        password = Hash.bcrypt(request.password),
        is_active="YES"  
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

def delete_user(db:Session,id:int):
    user=db.query(DbUser).filter(DbUser.user_id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
      
    db.delete(user)
    db.commit()
    return 'ok'    