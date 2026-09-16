import re
import unicodedata

from database import create_student


def normalize_text(value):
    normalized = unicodedata.normalize("NFKD", value)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    return re.sub(r"[^a-z0-9]", "", normalized)


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


name = input("Nome: ").strip()
surname = input("Sobrenome: ").strip()

if not name:
    print("Erro: o nome não pode ficar vazio.")
elif not surname:
    print("Erro: o sobrenome não pode ficar vazio.")
else:
    generated_email = (
        f"{normalize_text(name)}.{normalize_text(surname)}@example.com"
    )

    email = input(
        f"E-mail [{generated_email}]: "
    ).strip()

    if not email:
        email = generated_email

    if not is_valid_email(email):
        print("Erro: formato de e-mail inválido.")
    else:
        create_student(name, surname, email)
        print("Aluno cadastrado com sucesso.")