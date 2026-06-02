import os
import shutil
import logging
from core.classes.email import Email


class FileManager:
    def __init__(self, processed_base_dir: str):
        """
        :param processed_base_dir: Базовый путь для отсортированных писем
        """
        self.processed_base_dir = processed_base_dir

    def init_structure(self, categories: list):
        """
        Автоматически создает папки для всех категорий, если их еще нет на диске.
        """
        for category in categories:
            category_path = os.path.join(self.processed_base_dir, category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)
                logging.info(f"[FileManager] Инициализирована директория категории: {category_path}")

    def move_email(self, source_path: str, category: str, email: Email) -> str:
        """
        Перемещает файл в папку назначенной категории.
        Если файл с таким именем уже существует в целевой папке, добавляет уникальный суффикс.

        :param source_path: Текущий путь к файлу
        :param category: Папка назначения
        :param email: Экземпляр класса Email
        :return: Итоговый путь к перемещенному файлу
        """
        target_dir = os.path.join(self.processed_base_dir, category)

        base_name = email.file_name
        name_part, ext_part = os.path.splitext(base_name)

        target_path = os.path.join(target_dir, base_name)

        counter = 1
        while os.path.exists(target_path):
            new_name = f"{name_part}_{counter}{ext_part}"
            target_path = os.path.join(target_dir, new_name)
            counter += 1

        if counter > 1:
            logging.warning(f"[FileManager] Коллизия! Файл {base_name} сохранен как {os.path.basename(target_path)}")

        # Перенос файла
        try:
            shutil.move(source_path, target_path)
            logging.info(f"[FileManager] Файл успешно перемещен: {base_name} -> processed_mails/{category}/")
            return target_path
        except Exception as e:
            logging.error(f"[FileManager] КРИТИЧЕСКАЯ ОШИБКА при перемещении файла {base_name}: {str(e)}")
            raise e