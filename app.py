from database import create_student


name = input("Student name: ").strip()
email = input("Student email: ").strip()

if not name:
    print("Error: student name cannot be empty.")
elif not email:
    print("Error: student email cannot be empty.")
else:
    create_student(name, email)
    print("Student registered successfully.")