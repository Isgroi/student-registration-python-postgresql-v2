from getpass import getpass

import bcrypt

from database import get_connection


username = input("Nome do administrador: ").strip()
password = getpass("Senha do administrador: ").encode("utf-8")

password_hash = bcrypt.hashpw(
    password,
    bcrypt.gensalt(),
).decode("utf-8")

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, 'admin')
            ON CONFLICT (username) DO NOTHING;
            """,
            (username, password_hash),
        )

print("Administrador criado com sucesso.")