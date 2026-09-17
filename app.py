import re
import unicodedata

from rich.console import Console
from rich.table import Table

from database import (
    create_student,
    delete_student,
    get_student,
    list_students,
    search_students,
    update_student,
)


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


def edit_student():
    student_id = input("ID do aluno: ").strip()

    if not student_id.isdigit():
        print("Erro: o ID deve ser um número.")
        return

    student = get_student(int(student_id))

    if not student:
        print("Erro: aluno não encontrado.")
        return

    _, current_name, current_surname, current_email = student

    print("\nDados atuais:")
    print(f"Nome: {current_name}")
    print(f"Sobrenome: {current_surname}")
    print(f"E-mail: {current_email}")

    name = input(f"Novo nome [{current_name}]: ").strip()
    surname = input(
        f"Novo sobrenome [{current_surname}]: "
    ).strip()

    name = name or current_name
    surname = surname or current_surname

    if not is_valid_name(name):
        print("Erro: o nome deve conter apenas letras.")
        return

    if not is_valid_name(surname):
        print("Erro: o sobrenome deve conter apenas letras.")
        return

    generated_email = (
        f"{normalize_text(name)}.{normalize_text(surname)}@example.com"
    )

    print(f"E-mail sugerido: {generated_email}")

    email = input(
        f"Novo e-mail [{generated_email}]: "
    ).strip()

    email = email or generated_email

    if not is_valid_email(email):
        print("Erro: formato de e-mail inválido.")
        return

    updated = update_student(
    int(student_id),
    name,
    surname,
    email,
)

    if updated is True:
        print("Aluno atualizado com sucesso.")
    elif updated is False:
        print("Erro: aluno não encontrado.")
    else:
        print("Erro: este e-mail já está sendo usado.")

def remove_student():
    student_id = input("ID do aluno: ").strip()

    if not student_id.isdigit():
        print("Erro: o ID deve ser um número.")
        return

    student = get_student(int(student_id))

    if not student:
        print("Erro: aluno não encontrado.")
        return

    _, name, surname, email = student

    print("\nAluno selecionado:")
    print(f"Nome: {name} {surname}")
    print(f"E-mail: {email}")

    confirmation = input("Deseja realmente excluir? (s/n): ").strip().lower()

    if confirmation != "s":
        print("Exclusão cancelada.")
        return

    deleted = delete_student(int(student_id))

    if deleted:
        print("Aluno excluído com sucesso.")
    else:
        print("Erro: não foi possível excluir o aluno.")

while True:
    print("\n=== Registro de Alunos ===")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Buscar aluno")
    print("4 - Atualizar aluno")
    print("5 - Excluir aluno")
    print("0 - Sair")

    option = input("Escolha uma opção: ").strip()

    if option == "1":
        register_student()
    elif option == "2":
        show_students()
    elif option == "3":
        search_student()
    elif option == "4":
        edit_student()
    elif option == "5":
        remove_student()
    elif option == "0":
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida.")