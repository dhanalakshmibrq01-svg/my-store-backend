
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter,HTTPException,status
from db.database import get_db
from fastapi.param_functions import Depends
from db import models
from sqlalchemy.orm.session import Session
from db.hash import Hash
from auth import token_utils
from auth.active_users import current_logged_in_ids, set_active_user

router=APIRouter(
    #prefix="/auth",
    tags=['authentication']
)
@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user=db.query(models.DbUser).filter(models.DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    if not Hash.verify(user.password,request.password):   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")   

    current_logged_in_ids.add(user.user_id)
    
    
    set_active_user(db)
    # set_active_user(db, user.user_id)
    access_token = token_utils.create_access_token(data={'sub':user.username})
    

    return{
        'access_token':access_token,
        'token_type':'bearer',
        'user_id':user.user_id,
        'username':user.username,
        "is_active": "YES"

    }

@router.post("/logout")
def logout_user(user_id: int, db: Session = Depends(get_db)):
   
    current_logged_in_ids.discard(user_id)
    set_active_user(db)
    return {"msg": f"User {user_id} logged out successfully"}
