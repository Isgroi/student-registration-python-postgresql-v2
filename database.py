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
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO students (name, surname, email)
                VALUES (%s, %s, %s);
                """,
                (name, surname, email),
            )

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