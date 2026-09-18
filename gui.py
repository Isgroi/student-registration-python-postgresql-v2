import customtkinter as ctk
from tkinter import messagebox

from app import is_valid_email, is_valid_name, normalize_text
from database import create_student, list_students


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def register_student():
    name = name_entry.get().strip()
    surname = surname_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not surname:
        messagebox.showerror("Erro", "Nome e sobrenome são obrigatórios.")
        return

    if not is_valid_name(name):
        messagebox.showerror("Erro", "O nome deve conter apenas letras.")
        return

    if not is_valid_name(surname):
        messagebox.showerror("Erro", "O sobrenome deve conter apenas letras.")
        return

    if not email:
        email = (
            f"{normalize_text(name)}."
            f"{normalize_text(surname)}@example.com"
        )

    if not is_valid_email(email):
        messagebox.showerror("Erro", "Digite um e-mail válido.")
        return

    created = create_student(name, surname, email)

    if not created:
        messagebox.showerror(
            "Erro",
            "Este e-mail já está cadastrado.",
        )
        return

    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso.")

    name_entry.delete(0, "end")
    surname_entry.delete(0, "end")
    email_entry.delete(0, "end")

    refresh_students()


def refresh_students():
    for widget in students_frame.winfo_children():
        widget.destroy()

    students = list_students()

    total_label.configure(text=f"{len(students)} aluno(s) cadastrado(s)")

    headers = ["ID", "Nome", "Sobrenome", "E-mail"]

    for column, header in enumerate(headers):
        label = ctk.CTkLabel(
            students_frame,
            text=header,
            font=ctk.CTkFont(weight="bold"),
        )
        label.grid(row=0, column=column, padx=8, pady=8, sticky="w")

    for row, student in enumerate(students, start=1):
        student_id, name, surname, email = student
        values = [student_id, name, surname, email]

        for column, value in enumerate(values):
            label = ctk.CTkLabel(
                students_frame,
                text=str(value),
                anchor="w",
            )
            label.grid(
                row=row,
                column=column,
                padx=8,
                pady=5,
                sticky="w",
            )


window = ctk.CTk()
window.title("Registro de Alunos")
window.geometry("1050x600")
window.minsize(900, 500)

header = ctk.CTkFrame(window, fg_color="transparent")
header.pack(fill="x", padx=30, pady=(25, 10))

title = ctk.CTkLabel(
    header,
    text="Registro de Alunos",
    font=ctk.CTkFont(size=28, weight="bold"),
)
title.pack(side="left")

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

form_title = ctk.CTkLabel(
    form_frame,
    text="Novo cadastro",
    font=ctk.CTkFont(size=20, weight="bold"),
)
form_title.pack(padx=30, pady=(30, 25))

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

register_button = ctk.CTkButton(
    form_frame,
    text="Cadastrar aluno",
    width=300,
    height=42,
    command=register_student,
)
register_button.pack(padx=30, pady=(25, 10))

refresh_button = ctk.CTkButton(
    form_frame,
    text="Atualizar lista",
    width=300,
    height=38,
    fg_color="transparent",
    border_width=1,
    command=refresh_students,
)
refresh_button.pack(padx=30, pady=(0, 30))

list_frame = ctk.CTkFrame(content, corner_radius=18)
list_frame.pack(side="right", fill="both", expand=True)

list_title = ctk.CTkLabel(
    list_frame,
    text="Alunos cadastrados",
    font=ctk.CTkFont(size=20, weight="bold"),
)
list_title.pack(anchor="w", padx=25, pady=(25, 10))

students_frame = ctk.CTkScrollableFrame(list_frame)
students_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

students_frame.grid_columnconfigure(0, weight=0)
students_frame.grid_columnconfigure(1, weight=1)
students_frame.grid_columnconfigure(2, weight=1)
students_frame.grid_columnconfigure(3, weight=2)

refresh_students()

window.mainloop()