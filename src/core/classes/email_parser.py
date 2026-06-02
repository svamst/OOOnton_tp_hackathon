from src.core.classes.email import Email
import os
import json
import re
import logging

# ------------------------------------------------------------------------------------------------

class EmailParser:
    def __init__(self):
        self.binary_extensions = {'.jpeg', '.jpg', '.png', '.bin', '.exe', '.zip', '.rar'}

    def parse_file(self, file_path: str):
        """
        Безопасно читает файл, определяет его формат и извлекает тему и текст.
        Возвращает экземпляр класса email
        """

        file_name = os.path.basename(file_path)
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()

        tags = {
            "is_outlier": False,
            "error": False
        }

        if ext in self.binary_extensions:
            tags['is_outlier'] = True
            logging.info(f"[Parser] Файл {file_name} отсечен на этапе проверки расширения ({ext}).")
            email = Email(file_name=file_name, tags=tags)
            return email
        
        content = ""
        encodings = ['utf-8', 'utf-8-sig', 'cp1251', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read().strip()
                break

            except (UnicodeDecodeError, PermissionError):
                continue

        if not content:
            logging.warning(f"[Parser] Не удалось прочитать файл {file_name} как текст или файл пуст.")
            tags["is_outlier"] = True
            tags["error"] = True
            email = Email(tags=tags, file_name=file_name)
            return email
        
        if ext == '.json' or content.startswith('{'):
            try:
                json_data = json.loads(content)
                subject_topic = str(json_data.get("subject", json_data.get("Subject", ""))).strip()
                body = str(json_data.get("body", json_data.get("Body", content))).strip()
                logging.info(f"[Parser] Файл {file_name} успешно определен и распарсен как JSON.")
                email = Email(subject=subject_topic, body=body, tags=tags, file_name=file_name)
                return email
            
            except json.JSONDecodeError:
                if ext == '.json':
                    logging.error(f"[Parser] Файл {file_name} поврежден (битый JSON).")
                    tags["is_outlier"] = True
                    tags["error"] = True
                    email = Email(tags=tags, file_name=file_name)
                    return email
                
        # Ищем тему регулярным выражением
        subject_topic = re.search(
            r'^(?:Subject|Тема|Тема:|Subject:)\s*(.*)$',
            # текст после найденного "Subject" или "Тема" или "Тема:" или "Subject:" до конца строки
            content,
            re.IGNORECASE | re.MULTILINE
            # игнорирование регистра объединяется с многострочным режимом
        )
        
        if subject_topic:
            subject_topic = subject_topic.group(1).strip()

        logging.info(f"[Parser] Файл {file_name} успешно обработан как текстовое email-сообщение.")

        email = Email(subject=subject_topic, body=content, tags=tags, file_name=file_name)

        return email