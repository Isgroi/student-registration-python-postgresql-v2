import re
import unicodedata

from rich.console import Console
from rich.table import Table

from database import create_student, list_students


def normalize_text(value):
    normalized = unicodedata.normalize("NFKD", value)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    return re.sub(r"[^a-z0-9]", "", normalized)


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def register_student():
    name = input("Nome: ").strip()
    surname = input("Sobrenome: ").strip()

    if not name or not surname:
        print("Erro: nome e sobrenome são obrigatórios.")
        return

    generated_email = (
        f"{normalize_text(name)}.{normalize_text(surname)}@example.com"
    )

    email = input(f"E-mail [{generated_email}]: ").strip()
    email = email or generated_email

    if not is_valid_email(email):
        print("Erro: formato de e-mail inválido.")
        return

    create_student(name, surname, email)
    print("Aluno cadastrado com sucesso.")


def show_students():
    students = list_students()

    if not students:
        print("Nenhum aluno cadastrado.")
        return

    table = Table(title="Alunos cadastrados")

    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Nome", style="green")
    table.add_column("Sobrenome", style="green")
    table.add_column("E-mail", style="yellow")

    for student in students:
        student_id, name, surname, email = student
        table.add_row(str(student_id), name, surname, email)

    Console().print(table)


print("1 - Cadastrar aluno")
print("2 - Listar alunos")

option = input("Escolha uma opção: ").strip()

if option == "1":
    register_student()
elif option == "2":
    show_students()
else:
    print("Opção inválida.")