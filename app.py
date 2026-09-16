from database import get_connection


with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, email, created_at
            FROM students
            ORDER BY id;
            """
        )

        students = cursor.fetchall()


for student in students:
    print(student)
    