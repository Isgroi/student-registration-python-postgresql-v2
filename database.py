import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def create_student(name, surname, email):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO students (name, surname, email)
                    VALUES (%s, %s, %s);
                    """,
                    (name, surname, email),
                )
        return True

    except psycopg.errors.UniqueViolation:
        return False

def list_students():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, surname, email
                FROM students
                ORDER BY id;
                """
            )
            return cursor.fetchall()
def search_students(term):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, surname, email
                FROM students
                WHERE CAST(id AS TEXT) = %s
                   OR name ILIKE %s
                   OR surname ILIKE %s
                ORDER BY id;
                """,
                (term, f"%{term}%", f"%{term}%"),
            )
            return cursor.fetchall()
def update_student(student_id, name, surname, email):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE students
                SET name = %s,
                    surname = %s,
                    email = %s
                WHERE id = %s;
                """,
                (name, surname, email, student_id),
            )

            return cursor.rowcount > 0    

def get_student(student_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, surname, email
                FROM students
                WHERE id = %s;
                """,
                (student_id,),
            )
            return cursor.fetchone()      