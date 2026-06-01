import logging
from core.classes.email import Email
from config import (
    KEYWORDS_CRITICAL,
    KEYWORDS_SPAM,
    KEYWORDS_ROUTINE
)

# ---------------------------------------------------------------------------------------------------

class RulesClassifier:
    def __init__(self):
        self.keywords_critical = [k.lower() for k in KEYWORDS_CRITICAL]
        self.keywords_spam = [k.lower() for k in KEYWORDS_SPAM]
        self.keywords_routine = [k.lower() for k in KEYWORDS_ROUTINE]


    def _contains_any_keyword(self, text: str, keywords: list) -> bool:
        """Вспомогательный метод: проверяет, есть ли хотя бы одно ключевое слово в тексте."""
        for keyword in keywords:
            if keyword in text:
                return True
        return False


    def classify(self, email: Email) -> str:
        """
        Анализирует тему и тело письма и возвращает строку-категорию
        Входные данные:

        email: Экземпляр класса Email после парсинга

        return: Строка с названием категории
        """

        if email.tags.get("is_outlier") or email.tags.get("error"):
            logging.info(f"[Classifier] Файл {email.file_name} классифицирован как OUTLIER")
            return "outliers"

        subject_lower = email.subject.lower()
        body_lower = email.body.lower()
        full_text = f"{subject_lower} {body_lower}"

        if self._contains_any_keyword(full_text, self.keywords_critical):
            logging.info(f"[Classifier] Файл {email.file_name} классифицирован как CRITICAL_INCIDENTS")
            return "critical_incidents"

        if self._contains_any_keyword(full_text, self.keywords_spam):
            logging.info(f"[Classifier] Файл {email.file_name} классифицирован как SPAM_AND_PHISHING")
            return "spam_and_phishing"

        if self._contains_any_keyword(full_text, self.keywords_routine):
            logging.info(f"[Classifier] Файл {email.file_name} классифицирован как ROUTINE_REQUESTS")
            return "routine_requests"

        logging.warning(
            f"[Classifier] Для файла {email.file_name} не найдено явных правил. "
            f"Присвоена дефолтная категория: ROUTINE_REQUESTS."
        )
        
        return "routine_requests"