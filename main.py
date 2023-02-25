import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from mangum import Mangum


class Student(BaseModel):
    name: str
    subject: Literal["Physics", "Chemistry"]
    fees: float
    student_id: Optional[str] = uuid4().hex


STUDENTS_FILE = "students.json"
STUDENTS = []

if os.path.exists(STUDENTS_FILE):
    with open(STUDENTS_FILE, "r") as f:
        STUDENTS = json.load(f)

app = FastAPI()
handler = Mangum(app)


@app.get("/")
async def root():
    return {"message": "Welcome to Definite Success Classes!"}


@app.get("/random-student")
async def random_student():
    return random.choice(STUDENTS)


@app.get("/list-student")
async def list_student():
    return {"STUDENTS": STUDENTS}


@app.get("/student_by_index/{index}")
async def student_by_index(index: int):
    if index < len(STUDENTS):
        return STUDENTS[index]
    else:
        raise HTTPException(404, f"Student index {index} out of range ({len(STUDENTS)}).")


@app.post("/add-student")
async def add_student(student: Student):
    student.student_id = uuid4().hex
    json_book = jsonable_encoder(student)
    STUDENTS.append(json_book)

    with open(STUDENTS_FILE, "w") as f:
        json.dump(STUDENTS, f)

    return {"student_id": student.student_id}


@app.get("/get-student")
async def get_student(student_id: str):
    for student in STUDENTS:
        if student.student_id == student_id:
            return student

    raise HTTPException(404, f"Student ID {student_id} not found in database.")
