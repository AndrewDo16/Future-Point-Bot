import os

# Конфигурация подключения к PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),  # Имя базы данных
    "user": os.getenv("DB_USER"),  # Имя пользователя
    "password": os.getenv("DB_PASSWORD"),  # Пароль
    "host": os.getenv("DB_HOST"),  # Хост (имя сервиса)
    "port": os.getenv("DB_PORT", "5432")  # Порт (по умолчанию 5432)
}