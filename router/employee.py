

from fastapi import APIRouter, Body, HTTPException

router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

# Temporary in-memory storage
employees = []

# CREATE employee
@router.post("/")
def create_employee(
    fullname: str = Body(...),
    email: str = Body(...),
    dept_id: int = Body(...)
):
    employee = {
        "emp_id": len(employees) + 1,
        "fullname": fullname,
        "email": email,
        "dept_id": dept_id
    }

    employees.append(employee)
    return employee


# GET all employees
@router.get("/")
def get_all_employees():
    return employees


# GET employee by ID
@router.get("/{emp_id}")
def get_employee(emp_id: int):
    for emp in employees:
        if emp["emp_id"] == emp_id:
            return emp

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
