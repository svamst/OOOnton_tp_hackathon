import pytest
from src.core.classes.email import Email
from src.core.classes.rules_classifier import RulesClassifier
# Импортируем сам модуль классификатора, чтобы перехватить его локальные переменные для monkeypatch
import src.core.classes.rules_classifier as rc_module


@pytest.fixture(autouse=True)
def mock_config_keywords(monkeypatch):
    """
    Фикстура перехватывает ключевые слова прямо внутри модуля классификатора.
    Это решает проблему изолированного тестирования логики.
    """
    monkeypatch.setattr(rc_module, "KEYWORDS_CRITICAL", ["срочно", "critical", "авария"])
    monkeypatch.setattr(rc_module, "KEYWORDS_SPAM", ["выиграл", "крипта", "акция"])
    monkeypatch.setattr(rc_module, "KEYWORDS_ROUTINE", ["допуск", "мышка", "справка"])


def test_classify_outlier_or_error():
    """Если взведен флаг ломаного письма или ошибки, это 100% outliers."""
    classifier = RulesClassifier()
    
    email_outlier = Email(
        file_name="broken_1.txt", 
        subject="Срочно авария",
        body="Текст", 
        tags={"is_outlier": True, "error": False}
    )
    assert classifier.classify(email_outlier) == "outliers"

    email_error = Email(
        file_name="broken_2.txt", 
        subject="Обычная тема", 
        body="Текст", 
        tags={"is_outlier": False, "error": True}
    )
    assert classifier.classify(email_error) == "outliers"


def test_classify_critical_incidents():
    """Письмо содержит критическое слово и попадает в critical_incidents."""
    classifier = RulesClassifier()
    email = Email(
        file_name="mail_crit.txt", 
        subject="У нас АВАРИЯ в датацентре!", 
        body="Похоже, упали сервера.", 
        tags={"is_outlier": False, "error": False}
    )
    assert classifier.classify(email) == "critical_incidents"


def test_classify_spam_and_phishing():
    """Письмо содержит спам-слово и попадает в spam_and_phishing."""
    classifier = RulesClassifier()
    email = Email(
        file_name="mail_spam.txt", 
        subject="Поздравляем!", 
        body="Вы выиграли главный приз в нашей лотерее, заберите крипту.", 
        tags={"is_outlier": False, "error": False}
    )
    assert classifier.classify(email) == "spam_and_phishing"


def test_classify_routine_requests():
    """Письмо содержит рутинное слово и попадает в routine_requests."""
    classifier = RulesClassifier()
    email = Email(
        file_name="mail_routine.txt", 
        subject="Заявка", 
        body="Мне нужна новая мышка для работы.", 
        tags={"is_outlier": False, "error": False}
    )
    assert classifier.classify(email) == "routine_requests"


def test_classify_fallback_to_routine():
    """Если ни одно правило не подошло, срабатывает дефолтная категория routine_requests."""
    classifier = RulesClassifier()
    email = Email(
        file_name="mail_unknown.txt", 
        subject="Просто привет", 
        body="Как твои дела? Давно не виделись.", 
        tags={"is_outlier": False, "error": False}
    )
    assert classifier.classify(email) == "routine_requests"


def test_classify_case_insensitivity():
    """Классификатор должен игнорировать регистр букв (КаПс ЛоК)."""
    classifier = RulesClassifier()
    email = Email(
        file_name="caps.txt", 
        subject="СРОЧНО!!!", 
        body="Проверьте систему.", 
        tags={"is_outlier": False, "error": False}
    )
    assert classifier.classify(email) == "critical_incidents"