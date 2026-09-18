import tkinter as tk
from tkinter import messagebox

from app import is_valid_email, is_valid_name, normalize_text
from database import create_student


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

    if not is_valid_name(name):
        messagebox.showerror(
            "Erro",
            "O nome deve conter apenas letras.",
        )
        return

    if not is_valid_name(surname):
        messagebox.showerror(
            "Erro",
            "O sobrenome deve conter apenas letras.",
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

    created = create_student(name, surname, email)

    if not created:
        messagebox.showerror(
            "Erro",
            "Este e-mail já está cadastrado.",
        )
        return

    messagebox.showinfo(
        "Sucesso",
        "Aluno cadastrado com sucesso.",
    )

    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


window = tk.Tk()
window.title("Registro de Alunos")
window.geometry("500x350")

title = tk.Label(
    window,
    text="Cadastrar aluno",
    font=("Arial", 18, "bold"),
)
title.pack(pady=20)

name_label = tk.Label(window, text="Nome:")
name_label.pack()

name_entry = tk.Entry(window, width=40)
name_entry.pack(pady=5)

surname_label = tk.Label(window, text="Sobrenome:")
surname_label.pack()

surname_entry = tk.Entry(window, width=40)
surname_entry.pack(pady=5)

email_label = tk.Label(window, text="E-mail:")
email_label.pack()

email_entry = tk.Entry(window, width=40)
email_entry.pack(pady=5)

register_button = tk.Button(
    window,
    text="Cadastrar aluno",
    command=register_student,
)
register_button.pack(pady=20)

window.mainloop()