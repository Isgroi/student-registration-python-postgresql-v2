import bcrypt

from database import get_connection


def authenticate_user(username, password):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT username, password_hash, role
                FROM users
                WHERE username = %s;
                """,
                (username,),
            )

            user = cursor.fetchone()

    if not user:
        return None

    saved_username, password_hash, role = user

    password_is_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )

    if not password_is_valid:
        return None

    return {
        "username": saved_username,
        "role": role,
    }