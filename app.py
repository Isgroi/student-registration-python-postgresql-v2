import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, email, created_at FROM students;")
        students = cursor.fetchall()

for student in students:
    print(student)
    