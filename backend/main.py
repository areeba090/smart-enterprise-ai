from fastapi import FastAPI, Depends, HTTPException

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
from mongodb import client, db
from models import Employee, Department
from schemas import EmployeeResponse, DepartmentResponse
from qdrant_service import search_knowledge


app = FastAPI(title="Smart Enterprise Resource AI")


def get_db():
    db_session = SessionLocal()

    try:
        yield db_session
    finally:
        db_session.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    with engine.connect():
        print("PostgreSQL Connected Successfully")

    client.admin.command("ping")
    print("MongoDB Connected Successfully")


@app.get("/")
def root():
    return {
        "message": "Smart Enterprise Resource AI Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db_session: Session = Depends(get_db)):
    employees = db_session.query(Employee).all()

    return [
        EmployeeResponse(
            id=employee.id,
            name=employee.name,
            role=employee.role,
            expertise=employee.expertise,
            department=employee.department.name
            if employee.department
            else None
        )
        for employee in employees
    ]


# Search route must come before /employees/{employee_id}

@app.get("/employees/search", response_model=list[EmployeeResponse])
def search_employees(
    expertise: str,
    db_session: Session = Depends(get_db)
):
    employees = (
        db_session.query(Employee)
        .filter(Employee.expertise.ilike(f"%{expertise}%"))
        .all()
    )

    return [
        EmployeeResponse(
            id=employee.id,
            name=employee.name,
            role=employee.role,
            expertise=employee.expertise,
            department=employee.department.name
            if employee.department
            else None
        )
        for employee in employees
    ]


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db_session: Session = Depends(get_db)
):
    employee = (
        db_session.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return EmployeeResponse(
        id=employee.id,
        name=employee.name,
        role=employee.role,
        expertise=employee.expertise,
        department=employee.department.name
        if employee.department
        else None
    )


@app.get("/departments", response_model=list[DepartmentResponse])
def get_departments(db_session: Session = Depends(get_db)):
    departments = db_session.query(Department).all()

    return [
        DepartmentResponse(
            id=department.id,
            name=department.name,
            employee_count=len(department.employees)
        )
        for department in departments
    ]


@app.get("/knowledge")
def get_knowledge(category: str | None = None):
    query = {}

    if category:
        query["category"] = category

    documents = db.organizational_knowledge.find(
        query,
        {"_id": 0}
    )

    return list(documents)


@app.get("/knowledge/search")
def search_knowledge_endpoint(
    query: str,
    limit: int = 3
):
    results = search_knowledge(query, limit)

    return [
        {
            "title": result.payload.get("title"),
            "category": result.payload.get("category"),
            "content": result.payload.get("content"),
            "source": result.payload.get("source"),
            "score": result.score
        }
        for result in results
    ]