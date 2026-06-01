import os
import logging
import time
from collections import Counter

from src import config

from src.core.classes.email_parser import EmailParser
from src.core.classes.rules_classifier import RulesClassifier
from src.core.classes.file_manager import FileManager


def setup_logging():
    """
    Настраивает сквозное логирование в проекте.
    Логи одновременно пишутся в файл и выводятся в консоль.
    """

    os.makedirs(config.LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(config.LOG_FILE_PATH, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def main():
    setup_logging()
    logging.info("ЗАПУСК АЛГОРИТМА КЛАССИФИКАЦИИ ПИСЕМ")
    logging.info("")

    start_time = time.time()

    try:
        parser = EmailParser()
        classifier = RulesClassifier()
        file_manager = FileManager(processed_base_dir=config.PROCESSED_DIR)
        logging.info("[Main] Все компоненты успешно инициализированы.")

    except Exception as e:
        logging.critical(f"[Main] Ошибка при инициализации компонентов: {str(e)}", exc_info=True)
        return

    file_manager.init_structure(config.CATEGORIES)

    all_files = os.listdir(config.INBOX_DIR)
    files_to_process = [f for f in all_files if os.path.isfile(os.path.join(config.INBOX_DIR, f))]

    total_files = len(files_to_process)
    logging.info(f"[Main] Найдено файлов для обработки в inbox: {total_files}")

    if total_files == 0:
        logging.warning("[Main] Папка inbox пуста.")
        return

    stats_counter = Counter()
    success_count = 0
    failed_count = 0

    for index, file_name in enumerate(files_to_process, start=1):
        source_file_path = os.path.join(config.INBOX_DIR, file_name)

        logging.info(f"--- [{index}/{total_files}] Обработка файла: {file_name} ---")

        try:
            email_obj = parser.parse_file(source_file_path)
            assigned_category = classifier.classify(email_obj)
            file_manager.move_email(source_file_path, assigned_category, email_obj)

            stats_counter[assigned_category] += 1
            success_count += 1

        except Exception as e:
            logging.error(f"[Main] Критический сбой при обработке файла {file_name}: {str(e)}", exc_info=True)
            failed_count += 1
            continue

    end_time = time.time()
    execution_time = end_time - start_time

    logging.info("ВЫПОЛНЕНИЕ АЛГОРИТМА ЗАВЕРШЕНО")
    logging.info("")
    logging.info(f"Всего файлов обнаружено: {total_files}")
    logging.info(f"Успешно обработано:      {success_count}")
    logging.info(f"Ошибок обработки:        {failed_count}")
    logging.info(f"Общее время выполнения:  {execution_time:.2f} сек.")

    logging.info("")
    logging.info("РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ:")
    for category in config.CATEGORIES:
        count = stats_counter[category]
        logging.info(f"- {category}: {count}")
    logging.info("")


if name == "__main__":
    main()