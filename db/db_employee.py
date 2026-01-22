
# from fastapi import HTTPException,status
from schemas import EmployeeBase
from db.hash import Hash
from db.models import DbEmployee, DbUser, DbRole, DbDepartment
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# def create_employee(db: Session, request: EmployeeBase):

#     user = db.query(DbUser).filter(DbUser.user_id == request.user_id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     user.sr_id = 2
#     role = db.query(DbRole).filter(DbRole.role_id == request.role_id).first() 
#     if not role:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Role not found"
#         )

#     department = db.query(DbDepartment).filter(DbDepartment.id == request.department_id).first()
#     if not department:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Department not found"
#         )

#     new_employee = DbEmployee(
#         name=request.name,
#         phone_no=request.phone_no,
#         user_id=request.user_id,
#         role_id=request.role_id,
#         department_id=request.department_id  
#     )

   
#     db.add(new_employee)
#     db.commit()
#     db.refresh(new_employee)

#     return new_employee    
def create_employee(db: Session, request: EmployeeCreate):

    
    user = DbUser(
        username=request.username,
        password=Hash.bcrypt(request.password),
        sr_id=2,
        is_active = "NO"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

   
    employee = DbEmployee(
        name=request.name,
        phone_no=request.phone_no,
        user_id=user.user_id,
        department_id=request.department_id,
        role_id=request.role_id
    )
    db.add(employee)
    db.commit()

    return employee



def get_all_employees(db:Session):
    return db.query(DbEmployee).all()  

def get_employees(db:Session,emp_id:int):
    employee = db.query(DbEmployee).filter(DbEmployee.emp_id == emp_id).first() 
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with emp_id={emp_id} not found"
        )
    return employee

def update_employee(db: Session, emp_id: int, request: EmployeeUpdate):
    employee = db.query(DbEmployee).filter(DbEmployee.emp_id == emp_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee {emp_id} not found")

    if request.name is not None:
        employee.name = request.name

    if request.phone_no is not None:
        employee.phone_no = request.phone_no

    db.commit()
    db.refresh(employee)
    return employee



    
def delete_employee(db:Session,emp_id:int):
    employee = db.query(DbEmployee).filter(DbEmployee.emp_id == emp_id).first()  
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Employee with id={emp_id} not found"
        )
    db.delete(employee)
    db.commit()
    return 'ok'         