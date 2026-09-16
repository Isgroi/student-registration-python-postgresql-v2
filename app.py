import re
import unicodedata

from rich.console import Console
from rich.table import Table

from database import create_student, list_students, search_students


def normalize_text(value):
    normalized = unicodedata.normalize("NFKD", value)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    return re.sub(r"[^a-z0-9]", "", normalized)


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

def is_valid_name(value):
    pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[ '-][A-Za-zÀ-ÖØ-öø-ÿ]+)*$"
    return re.match(pattern, value) is not None


def register_student():
    while True:
        name = input("Nome: ").strip()

        if not name:
            print("Erro: o nome não pode ficar vazio.")
        elif not is_valid_name(name):
            print("Erro: o nome deve conter apenas letras.")
        else:
            break

    while True:
        surname = input("Sobrenome: ").strip()

        if not surname:
            print("Erro: o sobrenome não pode ficar vazio.")
        elif not is_valid_name(surname):
            print("Erro: o sobrenome deve conter apenas letras.")
        else:
            break

    generated_email = (
        f"{normalize_text(name)}.{normalize_text(surname)}@example.com"
    )

    email = input(f"E-mail [{generated_email}]: ").strip()
    email = email or generated_email

    if not is_valid_email(email):
        print("Erro: formato de e-mail inválido.")
        return

    created = create_student(name, surname, email)

    if created:
        print("Aluno cadastrado com sucesso.")
    else:
        print("Erro: este e-mail já está cadastrado.")


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

    for student_id, name, surname, email in students:
        table.add_row(
            str(student_id),
            name,
            surname,
            email,
        )

    Console().print(table)


def search_student():
    term = input("Digite o ID, nome ou sobrenome: ").strip()

    if not term:
        print("Erro: informe algo para pesquisar.")
        return

    students = search_students(term)

    if not students:
        print("Nenhum aluno encontrado.")
        return

    table = Table(title="Resultado da busca")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Nome", style="green")
    table.add_column("Sobrenome", style="green")
    table.add_column("E-mail", style="yellow")

    for student_id, name, surname, email in students:
        table.add_row(
            str(student_id),
            name,
            surname,
            email,
        )

    Console().print(table)


while True:
    print("\n=== Registro de Alunos ===")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Buscar aluno")
    print("0 - Sair")

    option = input("Escolha uma opção: ").strip()

    if option == "1":
        register_student()
    elif option == "2":
        show_students()
    elif option == "3":
        search_student()
    elif option == "0":
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida.")