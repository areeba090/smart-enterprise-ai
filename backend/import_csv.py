import csv

from database import SessionLocal
from models import Department, Employee


def import_csv_data():
    db = SessionLocal()

    try:
        # 1. Import departments
        with open("data/departments.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                department_name = row["name"].strip()

                existing = (
                    db.query(Department)
                    .filter(Department.name == department_name)
                    .first()
                )

                if not existing:
                    department = Department(name=department_name)
                    db.add(department)

        db.commit()

        # 2. Get departments from PostgreSQL
        departments = {
            department.name: department
            for department in db.query(Department).all()
        }

        # 3. Import employees
        with open("data/employees.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()

                existing = (
                    db.query(Employee)
                    .filter(Employee.name == name)
                    .first()
                )

                if not existing:
                    department_name = row["department"].strip()

                    department = departments.get(department_name)

                    if not department:
                        print(
                            f"Department not found for {name}: "
                            f"{department_name}"
                        )
                        continue

                    employee = Employee(
                        name=name,
                        role=row["role"].strip(),
                        expertise=row["expertise"].strip(),
                        department_id=department.id,
                    )

                    db.add(employee)

        db.commit()

        print("CSV data imported into PostgreSQL successfully.")

    except Exception as e:
        db.rollback()
        print("Import failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    import_csv_data()