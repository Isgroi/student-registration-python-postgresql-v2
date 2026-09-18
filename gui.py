import customtkinter as ctk
from tkinter import messagebox

from app import is_valid_email, is_valid_name, normalize_text
from database import create_student


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

    messagebox.showinfo(
        "Sucesso",
        "Aluno cadastrado com sucesso.",
    )

    name_entry.delete(0, "end")
    surname_entry.delete(0, "end")
    email_entry.delete(0, "end")


window = ctk.CTk()
window.title("Registro de Alunos")
window.geometry("600x500")
window.resizable(False, False)

card = ctk.CTkFrame(window, corner_radius=20)
card.pack(padx=60, pady=40, fill="both", expand=True)

title = ctk.CTkLabel(
    card,
    text="Registro de Alunos",
    font=ctk.CTkFont(size=28, weight="bold"),
)
title.pack(pady=(35, 5))

subtitle = ctk.CTkLabel(
    card,
    text="Cadastre um novo aluno",
    text_color="gray",
)
subtitle.pack(pady=(0, 30))

name_entry = ctk.CTkEntry(
    card,
    width=380,
    height=42,
    placeholder_text="Nome",
)
name_entry.pack(pady=8)

surname_entry = ctk.CTkEntry(
    card,
    width=380,
    height=42,
    placeholder_text="Sobrenome",
)
surname_entry.pack(pady=8)

email_entry = ctk.CTkEntry(
    card,
    width=380,
    height=42,
    placeholder_text="E-mail opcional",
)
email_entry.pack(pady=8)

register_button = ctk.CTkButton(
    card,
    text="Cadastrar aluno",
    width=380,
    height=42,
    corner_radius=10,
    command=register_student,
)
register_button.pack(pady=30)

window.mainloop()