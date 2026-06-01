#!/bin/bash

SCRIPT_NAME = "src/main.py"
LOG_DIR = "logs/lifetime"
LOG_FILE = "$LOG_DIR/run.log"

log_message() {
	echo "[$(date '+%d-%m-%Y %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_message "Классификатор писем запущен. Отслеживается процесс: $SCRIPT_NAME"

while true; do
	log_message "Запуск $SCRIPT_NAME"
	START_TIME = $(date +%s)

	python3 -u "$SCRIPT_NAME"

	EXIT_CODE = $?
	END_TIME = $(date +%s)
	DURATION = $((END_TIME - START_TIME))

	if [$DURATION -lt 60]; then
		TIME_STR = "${DURATION} секунд"
	else
		MINUTES = $((DURATION / 60))
		SECONDS = $((DURATION % 60))
		TIME_STR = "${MINUTES} минут {SECONDS} секунд"
	fi

	if [$EXIT_CODE -eq 0]; then
		log_message "Программа завершилась успешно. Время работы: $TIME_STR"
		log_message "Перезапуск через 5 секунд..."
		sleep 5
	else
		log_message "ОШИБКА: Программа упала с кодом $EXIT_CODE. Время работы: $TIME_STR"
		log_message "Перезапуск через 5 секунд..."
		sleep 5
	fi
done
