import database


def test_create_and_get_student(monkeypatch):
    monkeypatch.setenv(
        "DB_NAME",
        "student_registration_test",
    )

    email = "test.student@example.com"

    database.delete_student_by_email(email)

    created = database.create_student(
        "Test",
        "Student",
        email,
    )

    assert created is True

    students = database.search_students("Test")

    assert len(students) == 1
    assert students[0][1] == "Test"
    assert students[0][2] == "Student"
    assert students[0][3] == email

    database.delete_student_by_email(email)

def test_duplicate_email_is_rejected(monkeypatch):
    monkeypatch.setenv(
        "DB_NAME",
        "student_registration_test",
    )

    email = "duplicate.student@example.com"

    database.delete_student_by_email(email)

    first_created = database.create_student(
        "First",
        "Student",
        email,
    )

    second_created = database.create_student(
        "Second",
        "Student",
        email,
    )

    assert first_created is True
    assert second_created is False

    database.delete_student_by_email(email)