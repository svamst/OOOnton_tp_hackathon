#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

SCRIPT_NAME="$PROJECT_ROOT/src/main.py"
LOG_DIR="$PROJECT_ROOT/logs/lifetime"
LOG_FILE="$LOG_DIR/run.log"

mkdir -p "$LOG_DIR"

log_message() {
	echo "[$(date '+%d-%m-%Y %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_message "Классификатор писем запущен. Отслеживается процесс: $SCRIPT_NAME"

log_message "Запуск $SCRIPT_NAME"
START_TIME=$(date +%s)

python3 -u "$SCRIPT_NAME"

EXIT_CODE=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME-START_TIME))

if [ $DURATION -lt 60 ]; then
    TIME_STR="${DURATION} секунд"
else
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    TIME_STR="${MINUTES} минут ${SECONDS} секунд"
fi

if [ $EXIT_CODE -eq 0 ]; then
    log_message "Программа завершилась успешно. Время работы: $TIME_STR"
else
    log_message "ОШИБКА: Программа упала с кодом $EXIT_CODE. Время работы: $TIME_STR"
fi