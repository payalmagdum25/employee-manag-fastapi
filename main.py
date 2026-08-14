# from fastapi import FastAPI, Path, Body, HTTPException
# import sqlite3
# from pydantic import BaseModel, Field
# from typing import Annotated


# app = FastAPI()


# class Emp(BaseModel):
#     name: Annotated[str, Field(..., description="Name of employee")]
#     age: Annotated[int, Field(..., description="Age of employee")]
#     department: Annotated[str, Field(..., description="Department")]
#     salary: Annotated[float, Field(..., description="Salary")]
#     email: Annotated[str, Field(..., description="Email")]


# def get_connection():
#     conn = sqlite3.connect("employee.db")
#     conn.row_factory = sqlite3.Row
#     return conn


# def create_table():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS employee(
#         id TEXT PRIMARY KEY,
#         name TEXT,
#         age INTEGER,
#         department TEXT,
#         salary REAL,
#         email TEXT
#     )
#     """)

#     conn.commit()
#     conn.close()


# create_table()


# #load data

# def load_data():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM employee")
#     rows = cur.fetchall()

#     data = {}

#     for row in rows:
#         data[row["id"]] = {
#             "name": row["name"],
#             "age": row["age"],
#             "department": row["department"],
#             "salary": row["salary"],
#             "email": row["email"]
#         }

#     conn.close()

#     return data

# #hellomsg -- project name

# @app.get("/")
# def hello():
#     return {
#         "message": "Employee Management System"
#     }


# #about 
# @app.get("/about")
# def about():
#     return {
#         "message": "a fully functional api"
#     }

# #view 
# @app.get("/view")
# def view():
#     data = load_data()

#     return data

# #view single employee
# @app.get("/emp/{emp_id}")
# def view_emp(
#     emp_id: str = Path(
#         ...,
#         description="id of emp",
#         examples=["P001"]
#     )
# ):

#     data = load_data()

#     if emp_id in data:
#         return data[emp_id]

#     raise HTTPException(
#         status_code=404,
#         detail="Employee not found"
#     )

# #automate the id 
# def get_next_id():

#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT id
#         FROM employee
#         ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) DESC
#         LIMIT 1
#     """)

#     row = cur.fetchone()

#     if row:
#         last_id = int(row["id"][1:])
#         next_id = last_id + 1
#     else:
#         next_id = 1

#     conn.close()

#     return f"P{next_id:03d}"

# #create new employe
# @app.post("/create")
# def create_emp(employee: Emp):

#     employee_id = get_next_id()

#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO employee
#         (id, name, age, department, salary, email)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         employee_id,
#         employee.name,
#         employee.age,
#         employee.department,
#         employee.salary,
#         employee.email
#     ))

#     conn.commit()
#     conn.close()

#     return {
#         "message": "Employee created successfully",
#         "id": employee_id
#     }

# #update 
# @app.put("/update/{emp_id}")
# def update_emp(
#     emp_id: str,
#     employee: dict = Body(...)
# ):

#     data = load_data()

#     # Check employee exists
#     if emp_id not in data:
#         raise HTTPException(
#             status_code=404,
#             detail="Employee not found"
#         )

  
#     allowed_fields = [
#         "name",
#         "age",
#         "department",
#         "salary",
#         "email"
#     ]

  
#     for key in employee.keys():

#         if key not in allowed_fields:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Invalid field: {key}"
#             )

    
#     if not employee:
#         raise HTTPException(
#             status_code=400,
#             detail="Please provide at least one field to update"
#         )

#     conn = get_connection()
#     cur = conn.cursor()

#     # Update fields
#     for key, value in employee.items():

#         query = f"""
#             UPDATE employee
#             SET {key} = ?
#             WHERE id = ?
#         """

#         cur.execute(
#             query,
#             (value, emp_id)
#         )

#     conn.commit()
#     conn.close()


#     data = load_data()

#     return {
#         "message": "Employee updated successfully",
#         "id": emp_id,
#         "data": data[emp_id]
#     }


# #delete employe

# @app.delete("/delete/{emp_id}")
# def delete_emp(emp_id: str):

#     data = load_data()


  
#     if emp_id not in data:
#         raise HTTPException(
#             status_code=404,
#             detail="Employee not found"
#         )

#     deleted_emp = data[emp_id]

#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "DELETE FROM employee WHERE id = ?",
#         (emp_id,)
#     )

#     conn.commit()
#     conn.close()

#     return {
#         "message": "Employee deleted successfully",
#         "deleted_emp": deleted_emp
#     }


from typing import Annotated

import sqlite3

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, EmailStr, Field


app = FastAPI(
    title="Employee Management API",
    description="A FastAPI application for managing employees",
    version="1.0.0",
)


DATABASE = "employee.db"


class EmployeeCreate(BaseModel):
    name: Annotated[
        str,
        Field(..., min_length=2, max_length=100, description="Employee name"),
    ]

    age: Annotated[
        int,
        Field(..., ge=18, le=100, description="Employee age"),
    ]

    department: Annotated[
        str,
        Field(..., min_length=2, max_length=100, description="Department"),
    ]

    salary: Annotated[
        float,
        Field(..., ge=0, description="Employee salary"),
    ]

    email: Annotated[
        EmailStr,
        Field(..., description="Employee email"),
    ]


class EmployeeUpdate(BaseModel):
    name: Annotated[
        str | None,
        Field(None, min_length=2, max_length=100),
    ]

    age: Annotated[
        int | None,
        Field(None, ge=18, le=100),
    ]

    department: Annotated[
        str | None,
        Field(None, min_length=2, max_length=100),
    ]

    salary: Annotated[
        float | None,
        Field(None, ge=0),
    ]

    email: Annotated[
        EmailStr | None,
        Field(None),
    ]


def get_connection():
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """Create the employee table if it does not exist."""
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employee(
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                email TEXT NOT NULL
            )
            """
        )

        # Add email column if an older database does not have it.
        cursor.execute("PRAGMA table_info(employee)")
        columns = [row["name"] for row in cursor.fetchall()]

        if "email" not in columns:
            cursor.execute(
                "ALTER TABLE employee ADD COLUMN email TEXT DEFAULT ''"
            )

        connection.commit()

    finally:
        connection.close()


def load_data():
    """Load all employees from the database."""
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employee")
        rows = cursor.fetchall()

        data = {}

        for row in rows:
            data[row["id"]] = {
                "name": row["name"],
                "age": row["age"],
                "department": row["department"],
                "salary": row["salary"],
                "email": row["email"],
            }

        return data

    finally:
        connection.close()


def get_next_id():
    """Generate the next employee ID."""
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM employee
            ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        if row:
            last_id = int(row["id"][1:])
            next_id = last_id + 1
        else:
            next_id = 1

        return f"P{next_id:03d}"

    finally:
        connection.close()


create_table()


@app.get("/")
def hello():
    """Return the API welcome message."""
    return {
        "message": "Employee Management System"
    }


@app.get("/about")
def about():
    """Return information about the API."""
    return {
        "message": "A fully functional Employee Management API"
    }


@app.get("/view")
def view():
    """Return all employees."""
    return load_data()


@app.get("/emp/{emp_id}")
def view_emp(
    emp_id: str = Path(
        ...,
        description="Employee ID",
        examples=["P001"],
    )
):
    """Return one employee by ID."""
    data = load_data()

    if emp_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return data[emp_id]


@app.post("/create", status_code=201)
def create_emp(employee: EmployeeCreate):
    """Create a new employee."""
    employee_id = get_next_id()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO employee
            (id, name, age, department, salary, email)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                employee_id,
                employee.name,
                employee.age,
                employee.department,
                employee.salary,
                str(employee.email),
            ),
        )

        connection.commit()

    finally:
        connection.close()

    return {
        "message": "Employee created successfully",
        "id": employee_id,
    }


@app.put("/update/{emp_id}")
def update_emp(
    emp_id: str,
    employee: EmployeeUpdate,
):
    """Update one or more fields of an employee."""
    data = load_data()

    if emp_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    update_data = employee.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least one field to update",
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        update_queries = {
            "name": "UPDATE employee SET name = ? WHERE id = ?",
            "age": "UPDATE employee SET age = ? WHERE id = ?",
            "department": "UPDATE employee SET department = ? WHERE id = ?",
            "salary": "UPDATE employee SET salary = ? WHERE id = ?",
            "email": "UPDATE employee SET email = ? WHERE id = ?",
        }

        for field, value in update_data.items():
            query = update_queries[field]

            if field == "email":
                value = str(value)

            cursor.execute(
                query,
                (value, emp_id),
            )

        connection.commit()

    finally:
        connection.close()

    data = load_data()

    return {
        "message": "Employee updated successfully",
        "id": emp_id,
        "data": data[emp_id],
    }


@app.delete("/delete/{emp_id}")
def delete_emp(emp_id: str):
    """Delete an employee by ID."""
    data = load_data()

    if emp_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    deleted_employee = data[emp_id]

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM employee WHERE id = ?",
            (emp_id,),
        )

        connection.commit()

    finally:
        connection.close()

    return {
        "message": "Employee deleted successfully",
        "deleted_emp": deleted_employee,
    }