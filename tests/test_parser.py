import os
import pytest
from src.core.classes.email_parser import EmailParser
from src.core.classes.email import Email

@pytest.fixture
def parser():
    """Фикстура для инициализации парсера перед каждым тестом"""
    return EmailParser()


def test_parse_valid_email(tmp_path, parser):
    """Проверка успешного парсинга стандартного корректного письма"""
    email_content = (
        "From: ivan@company.ru\n"
        "Subject: Запрос доступа к Jira\n"
        "\n"
        "Привет! Добавьте, пожалуйста, в проект PROJ."
    )
    test_file = tmp_path / "valid_mail.txt"
    test_file.write_text(email_content, encoding="utf-8")

    email_obj = parser.parse_file(str(test_file))

    assert isinstance(email_obj, Email)
    assert email_obj.file_name == "valid_mail.txt"
    assert email_obj.subject == ": Запрос доступа к Jira"
    assert "Привет! Добавьте, пожалуйста" in email_obj.body
    assert email_obj.tags.get("is_outlier") is False
    assert email_obj.tags.get("error") is False


def test_parse_empty_file_as_outlier(tmp_path, parser):
    """Пустой файл должен распознаваться как выброс"""
    test_file = tmp_path / "empty_corrupted.txt"
    test_file.write_text("", encoding="utf-8")

    email_obj = parser.parse_file(str(test_file))

    assert isinstance(email_obj, Email)
    assert email_obj.file_name == "empty_corrupted.txt"
    assert (email_obj.tags.get("is_outlier") is True) or ("error" in email_obj.tags)


def test_parse_missing_fields_fallback(tmp_path, parser):
    """Если в письме нет явной темы (Subject), парсер не должен падать"""
    email_content = "Просто какой-то текст без заголовков и Subject."
    test_file = tmp_path / "no_headers.txt"
    test_file.write_text(email_content, encoding="utf-8")

    email_obj = parser.parse_file(str(test_file))

    assert isinstance(email_obj, Email)
    assert email_obj.file_name == "no_headers.txt"
    assert email_obj.subject == None
    assert "Просто какой-то текст" in email_obj.body