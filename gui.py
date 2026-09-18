import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from app import is_valid_email, is_valid_name, normalize_text
from auth import authenticate_user
from database import (
    create_student,
    delete_student,
    get_student,
    list_students,
    update_student,
)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def show_dashboard(user):
    window = ctk.CTk()
    window.title("Registro de Alunos")
    window.geometry("1100x600")

    def show_error(message):
        CTkMessagebox(
            title="Erro",
            message=str(message),
            icon="cancel",
            width=420,
            height=220,
        )

    def show_success(message):
        CTkMessagebox(
            title="Sucesso",
            message=str(message),
            icon="check",
        )

    def edit_selected_student(student_id):
        student = get_student(student_id)

        if not student:
            show_error("Aluno não encontrado.")
            return

        _, current_name, current_surname, current_email = student

        edit_window = ctk.CTkToplevel(window)
        edit_window.title("Editar aluno")
        edit_window.geometry("450x450")
        edit_window.resizable(False, False)
        edit_window.grab_set()

        ctk.CTkLabel(
            edit_window,
            text="✎ Editar aluno",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        ).pack(pady=(30, 25))

        name_input = ctk.CTkEntry(
            edit_window,
            width=300,
            height=42,
            placeholder_text="Nome",
        )
        name_input.pack(pady=8)
        name_input.insert(0, current_name)

        surname_input = ctk.CTkEntry(
            edit_window,
            width=300,
            height=42,
            placeholder_text="Sobrenome",
        )
        surname_input.pack(pady=8)
        surname_input.insert(0, current_surname)

        email_input = ctk.CTkEntry(
            edit_window,
            width=300,
            height=42,
            placeholder_text="E-mail",
        )
        email_input.pack(pady=8)
        email_input.insert(0, current_email)

        def save_changes():
            name = name_input.get().strip().title()
            surname = surname_input.get().strip().title()
            email = email_input.get().strip()

            if not name or not surname:
                show_error("Nome e sobrenome são obrigatórios.")
                return

            if not is_valid_name(name):
                show_error("O nome deve conter apenas letras.")
                return

            if not is_valid_name(surname):
                show_error("O sobrenome deve conter apenas letras.")
                return

            if not email:
                email = (
                    f"{normalize_text(name)}."
                    f"{normalize_text(surname)}@example.com"
                )

            if not is_valid_email(email):
                show_error("Digite um e-mail válido.")
                return

            updated = update_student(
                student_id,
                name,
                surname,
                email,
            )

            if updated is None:
                show_error("Este e-mail já está sendo usado.")
                return

            if not updated:
                show_error("Aluno não encontrado.")
                return

            show_success("Aluno atualizado com sucesso.")
            edit_window.destroy()
            refresh_students()

        ctk.CTkButton(
            edit_window,
            text="Salvar alterações",
            width=300,
            height=42,
            command=save_changes,
        ).pack(pady=(25, 10))

        ctk.CTkButton(
            edit_window,
            text="Cancelar",
            width=300,
            height=38,
            fg_color="transparent",
            border_width=1,
            command=edit_window.destroy,
        ).pack()

    def delete_selected_student(student_id):
        student = get_student(student_id)

        if not student:
            show_error("Aluno não encontrado.")
            return

        _, name, surname, email = student

        confirmation = CTkMessagebox(
            title="Confirmar exclusão",
            message=f"Excluir {name} {surname}?\n\n{email}",
            icon="question",
            option_1="Cancelar",
            option_2="Excluir",
        ).get()

        if confirmation != "Excluir":
            return

        if delete_student(student_id):
            show_success("Aluno excluído com sucesso.")
            refresh_students()
        else:
            show_error("Não foi possível excluir o aluno.")

    def refresh_students():
        for widget in students_frame.winfo_children():
            widget.destroy()

        students = list_students()

        total_label.configure(
            text=f"{len(students)} aluno(s) cadastrado(s)"
        )

        headers = [
            "ID",
            "Nome",
            "Sobrenome",
            "E-mail",
            "Editar",
            "Excluir",
        ]

        for column, header in enumerate(headers):
            ctk.CTkLabel(
                students_frame,
                text=header,
                font=ctk.CTkFont(weight="bold"),
            ).grid(
                row=0,
                column=column,
                padx=8,
                pady=8,
                sticky="w",
            )

        for row, student in enumerate(students, start=1):
            student_id, name, surname, email = student
            values = [student_id, name, surname, email]

            for column, value in enumerate(values):
                ctk.CTkLabel(
                    students_frame,
                    text=str(value),
                    anchor="w",
                ).grid(
                    row=row,
                    column=column,
                    padx=8,
                    pady=5,
                    sticky="w",
                )

            ctk.CTkButton(
                students_frame,
                text="✎ Editar",
                width=80,
                height=28,
                command=lambda current_id=student_id:
                    edit_selected_student(current_id),
            ).grid(
                row=row,
                column=4,
                padx=4,
                pady=5,
            )

            ctk.CTkButton(
                students_frame,
                text="🗑 Excluir",
                width=90,
                height=28,
                fg_color="#b83232",
                hover_color="#922b2b",
                command=lambda current_id=student_id:
                    delete_selected_student(current_id),
            ).grid(
                row=row,
                column=5,
                padx=4,
                pady=5,
            )

    def register_student():
        name = name_entry.get().strip().title()
        surname = surname_entry.get().strip().title()
        email = email_entry.get().strip()

        if not name or not surname:
            show_error("Nome e sobrenome são obrigatórios.")
            return

        if not is_valid_name(name):
            show_error("O nome deve conter apenas letras.")
            return

        if not is_valid_name(surname):
            show_error("O sobrenome deve conter apenas letras.")
            return

        if not email:
            email = (
                f"{normalize_text(name)}."
                f"{normalize_text(surname)}@example.com"
            )

        if not is_valid_email(email):
            show_error("Digite um e-mail válido.")
            return

        if not create_student(name, surname, email):
            show_error("Este e-mail já está cadastrado.")
            return

        show_success("Aluno cadastrado com sucesso.")

        name_entry.delete(0, "end")
        surname_entry.delete(0, "end")
        email_entry.delete(0, "end")

        refresh_students()

    header = ctk.CTkFrame(
        window,
        fg_color="transparent",
    )
    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10),
    )

    ctk.CTkLabel(
        header,
        text=f"Olá, {user['username']}",
        font=ctk.CTkFont(
            size=28,
            weight="bold",
        ),
    ).pack(side="left")

    total_label = ctk.CTkLabel(
        header,
        text="0 aluno(s) cadastrado(s)",
        text_color="gray",
    )
    total_label.pack(
        side="right",
        pady=8,
    )

    content = ctk.CTkFrame(
        window,
        fg_color="transparent",
    )
    content.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=15,
    )

    form_frame = ctk.CTkFrame(
        content,
        corner_radius=18,
    )
    form_frame.pack(
        side="left",
        fill="y",
        padx=(0, 15),
    )

    ctk.CTkLabel(
        form_frame,
        text="Novo cadastro",
        font=ctk.CTkFont(
            size=20,
            weight="bold",
        ),
    ).pack(
        padx=30,
        pady=(30, 25),
    )

    name_entry = ctk.CTkEntry(
        form_frame,
        width=300,
        height=42,
        placeholder_text="Nome",
    )
    name_entry.pack(
        padx=30,
        pady=8,
    )

    surname_entry = ctk.CTkEntry(
        form_frame,
        width=300,
        height=42,
        placeholder_text="Sobrenome",
    )
    surname_entry.pack(
        padx=30,
        pady=8,
    )

    email_entry = ctk.CTkEntry(
        form_frame,
        width=300,
        height=42,
        placeholder_text="E-mail opcional",
    )
    email_entry.pack(
        padx=30,
        pady=8,
    )

    ctk.CTkButton(
        form_frame,
        text="Cadastrar aluno",
        width=300,
        height=42,
        command=register_student,
    ).pack(
        padx=30,
        pady=(25, 10),
    )

    ctk.CTkButton(
        form_frame,
        text="Atualizar lista",
        width=300,
        height=38,
        fg_color="transparent",
        border_width=1,
        command=refresh_students,
    ).pack(
        padx=30,
        pady=(0, 30),
    )

    list_frame = ctk.CTkFrame(
        content,
        corner_radius=18,
    )
    list_frame.pack(
        side="right",
        fill="both",
        expand=True,
    )

    ctk.CTkLabel(
        list_frame,
        text="Alunos cadastrados",
        font=ctk.CTkFont(
            size=20,
            weight="bold",
        ),
    ).pack(
        anchor="w",
        padx=25,
        pady=(25, 10),
    )

    students_frame = ctk.CTkScrollableFrame(list_frame)
    students_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15),
    )

    refresh_students()
    window.mainloop()


def show_login():
    window = ctk.CTk()
    window.title("Login - Registro de Alunos")
    window.geometry("450x400")
    window.resizable(False, False)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            CTkMessagebox(
                title="Erro",
                message="Informe usuário e senha.",
                icon="cancel",
            )
            return

        user = authenticate_user(
            username,
            password,
        )

        if not user:
            CTkMessagebox(
                title="Erro",
                message="Usuário ou senha inválidos.",
                icon="cancel",
            )
            return

        window.destroy()
        show_dashboard(user)

    card = ctk.CTkFrame(
        window,
        corner_radius=18,
    )
    card.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=40,
    )

    ctk.CTkLabel(
        card,
        text="Acesso administrativo",
        font=ctk.CTkFont(
            size=24,
            weight="bold",
        ),
    ).pack(
        pady=(35, 25),
    )

    username_entry = ctk.CTkEntry(
        card,
        width=300,
        height=42,
        placeholder_text="Usuário",
    )
    username_entry.pack(pady=8)

    password_entry = ctk.CTkEntry(
        card,
        width=300,
        height=42,
        placeholder_text="Senha",
        show="*",
    )
    password_entry.pack(pady=8)

    ctk.CTkButton(
        card,
        text="Entrar",
        width=300,
        height=42,
        command=login,
    ).pack(pady=25)

    window.mainloop()


if __name__ == "__main__":
    show_login()