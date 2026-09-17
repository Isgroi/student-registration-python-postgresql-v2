from app import is_valid_email, is_valid_name, normalize_text


def test_normalize_text_removes_accents():
    assert normalize_text("João") == "joao"


def test_valid_name_accepts_letters():
    assert is_valid_name("Ana") is True
    assert is_valid_name("Maria Silva") is True


def test_valid_name_rejects_numbers():
    assert is_valid_name("Ana123") is False


def test_valid_email_accepts_valid_format():
    assert is_valid_email("ana.silva@example.com") is True
    assert is_valid_email("user123@example.com") is True


def test_valid_email_rejects_invalid_format():
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("user@example") is False