
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from db.models import SystemRole
from schemas import SystemRoleDisplay

router = APIRouter(prefix="/system-roles", tags=["System Roles"])

@router.get("/", response_model=List[SystemRoleDisplay])
def get_system_roles(db: Session = Depends(get_db)):
    return db.query(SystemRole).all()
