#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv  # Импортируем load_dotenv

# Указываем путь к файлу .env, который находится в той же директории, что и manage.py
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Загружаем переменные окружения из файла .env, если он существует
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsoccergame.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
