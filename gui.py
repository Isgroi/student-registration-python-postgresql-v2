import customtkinter as ctk
from tkinter import messagebox

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
    window.geometry("1050x600")


    def delete_selected_student(student_id):
        student = get_student(student_id)

        if not student:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return

        _, name, surname, email = student

        confirm = messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir {name} {surname}?\n\n{email}",
        )

        if not confirm:
            return

        if delete_student(student_id):
            messagebox.showinfo(
                "Sucesso",
                "Aluno excluído com sucesso.",
            )
            refresh_students()
        else:
            messagebox.showerror(
                "Erro",
                "Não foi possível excluir o aluno.",
            )


    def refresh_students():
        for widget in students_frame.winfo_children():
            widget.destroy()

        students = list_students()

        total_label.configure(
            text=f"{len(students)} aluno(s) cadastrado(s)"
        )

        headers = ["ID", "Nome", "Sobrenome", "E-mail", "Ações"]

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
                text="Excluir",
                width=70,
                height=28,
                fg_color="#b83232",
                hover_color="#922b2b",
                command=lambda current_id=student_id:
                    delete_selected_student(current_id),
            ).grid(
                row=row,
                column=4,
                padx=8,
                pady=5,
            )

    def register_student():
        name = name_entry.get().strip()
        surname = surname_entry.get().strip()
        email = email_entry.get().strip()

        if not name or not surname:
            messagebox.showerror(
                "Erro",
                "Nome e sobrenome são obrigatórios.",
            )
            return

        if not is_valid_name(name) or not is_valid_name(surname):
            messagebox.showerror(
                "Erro",
                "Nome e sobrenome devem conter apenas letras.",
            )
            return

        if not email:
            email = (
                f"{normalize_text(name)}."
                f"{normalize_text(surname)}@example.com"
            )

        if not is_valid_email(email):
            messagebox.showerror(
                "Erro",
                "Digite um e-mail válido.",
            )
            return

        if not create_student(name, surname, email):
            messagebox.showerror(
                "Erro",
                "Este e-mail já está cadastrado.",
            )
            return

        messagebox.showinfo(
            "Sucesso",
            "Aluno cadastrado com sucesso.",
        )

        name_entry.delete(0, "end")
        surname_entry.delete(0, "end")
        email_entry.delete(0, "end")
        refresh_students()

    header = ctk.CTkFrame(window, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header,
        text=f"Olá, {user['username']}",
        font=ctk.CTkFont(size=28, weight="bold"),
    ).pack(side="left")

    total_label = ctk.CTkLabel(
        header,
        text="0 aluno(s) cadastrado(s)",
        text_color="gray",
    )
    total_label.pack(side="right", pady=8)

    content = ctk.CTkFrame(window, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=30, pady=15)

    form_frame = ctk.CTkFrame(content, corner_radius=18)
    form_frame.pack(side="left", fill="y", padx=(0, 15))

    ctk.CTkLabel(
        form_frame,
        text="Novo cadastro",
        font=ctk.CTkFont(size=20, weight="bold"),
    ).pack(padx=30, pady=(30, 25))

    name_entry = ctk.CTkEntry(
        form_frame,
        width=300,
        height=42,
        placeholder_text="Nome",
    )
    name_entry.pack(padx=30, pady=8)

    surname_entry = ctk.CTkEntry(
        form_frame,
        width=300,
        height=42,
        placeholder_text="Sobrenome",
    )
    surname_entry.pack(padx=30, pady=8)

    email_entry = ctk.CTkEntry(
        form_frame,
        width=300,
        height=42,
        placeholder_text="E-mail opcional",
    )
    email_entry.pack(padx=30, pady=8)

    ctk.CTkButton(
        form_frame,
        text="Cadastrar aluno",
        width=300,
        height=42,
        command=register_student,
    ).pack(padx=30, pady=(25, 10))

    ctk.CTkButton(
        form_frame,
        text="Atualizar lista",
        width=300,
        height=38,
        fg_color="transparent",
        border_width=1,
        command=refresh_students,
    ).pack(padx=30, pady=(0, 30))

    list_frame = ctk.CTkFrame(content, corner_radius=18)
    list_frame.pack(side="right", fill="both", expand=True)

    ctk.CTkLabel(
        list_frame,
        text="Alunos cadastrados",
        font=ctk.CTkFont(size=20, weight="bold"),
    ).pack(anchor="w", padx=25, pady=(25, 10))

    students_frame = ctk.CTkScrollableFrame(list_frame)
    students_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

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

        user = authenticate_user(username, password)

        if not user:
            messagebox.showerror(
                "Erro",
                "Usuário ou senha inválidos.",
            )
            return

        window.destroy()
        show_dashboard(user)

    card = ctk.CTkFrame(window, corner_radius=18)
    card.pack(fill="both", expand=True, padx=40, pady=40)

    ctk.CTkLabel(
        card,
        text="Acesso administrativo",
        font=ctk.CTkFont(size=24, weight="bold"),
    ).pack(pady=(35, 25))

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