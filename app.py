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


name = input("First name: ").strip()
surname = input("Surname: ").strip()

if not name:
    print("Error: first name cannot be empty.")
elif not surname:
    print("Error: surname cannot be empty.")
else:
    generated_email = (
        f"{normalize_text(name)}.{normalize_text(surname)}@example.com"
    )

    email = input(
        f"Email [{generated_email}]: "
    ).strip()

    if not email:
        email = generated_email

    if not is_valid_email(email):
        print("Error: invalid email format.")
    else:
        create_student(name, surname, email)
        print("Student registered successfully.")