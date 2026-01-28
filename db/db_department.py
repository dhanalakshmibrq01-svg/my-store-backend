

from schemas import DepartmentBase
from db.models import DbDepartment
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

def create_dept(db: Session, request: DepartmentBase):
    if not request.code or not request.code.strip() or request.code.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department code cannot be empty or default value"
        )


    if not request.name or not request.name.strip() or request.name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name cannot be empty or default value"
    )
    

    if db.query(DbDepartment).filter(
        DbDepartment.code.ilike(request.code.strip())).first():
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Department code already exists"
    )


    if db.query(DbDepartment).filter(
       DbDepartment.name.ilike(request.name.strip())).first():
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Department name already exists"
    )

    new_dept = DbDepartment(
        code=request.code,
        name = request.name
    )
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

def get_all_depts(db:Session):
    return db.query(DbDepartment).all() 

def get_dept(db:Session,id:int):
    dept = db.query(DbDepartment).filter(DbDepartment.id == id).first()  
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id={id} not found"
        )
    return dept

def update_dept(db: Session, id: int, request: DepartmentBase):
    
    dept = db.query(DbDepartment).filter(DbDepartment.id == id).first()  
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Department with id={id} not found"
        )
    if not request.code or not request.code.strip() or request.code.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department code cannot be empty or default value"
        )

    
    if not request.name or not request.name.strip() or request.name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name cannot be empty or default value"
        )    
    
    dept.code = request.code
    dept.name = request.name
    
    db.commit() 
    db.refresh(dept)  

    
    return {
        "id": dept.id,
        "code": dept.code,
        "name": dept.name
    }

def delete_dept(db:Session,id:int):
    
    dept = db.query(DbDepartment).filter(DbDepartment.id == id).first()  
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Department with id={id} not found"
        )
    db.delete(dept)
    db.commit()
    return 'ok' 
