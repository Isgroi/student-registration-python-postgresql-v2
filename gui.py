import tkinter as tk


def main():
    window = tk.Tk()
    window.title("Registro de Alunos")
    window.geometry("700x450")

    title = tk.Label(
        window,
        text="Registro de Alunos",
        font=("Arial", 18, "bold"),
    )
    title.pack(pady=30)

    message = tk.Label(
        window,
        text="Interface gráfica em construção.",
        font=("Arial", 12),
    )
    message.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()