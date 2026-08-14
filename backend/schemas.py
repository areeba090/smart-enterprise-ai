from pydantic import BaseModel


class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str
    expertise: str | None = None
    department: str | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    employee_count: int