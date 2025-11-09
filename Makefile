.PHONY: help install venv migrate run test lint clean format db-upgrade db-downgrade db-revision superuser

# Цвета для вывода
BLUE = \033[0;34m
GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m # No Color

help:
  @echo "$(BLUE)Доступные команды:$(NC)"
  @echo "$(GREEN)make install$(NC)        - Установить все зависимости"
  @echo "$(GREEN)make venv$(NC)           - Создать виртуальное окружение"
  @echo "$(GREEN)make run$(NC)            - Запустить приложение"
  @echo "$(GREEN)make test$(NC)           - Запустить тесты"
  @echo "$(GREEN)make lint$(NC)           - Проверить код с помощью flake8"
  @echo "$(GREEN)make format$(NC)         - Отформатировать код"
  @echo "$(GREEN)make clean$(NC)          - Очистить кэш и временные файлы"
  @echo "$(GREEN)make migrate$(NC)        - Применить миграции"
  @echo "$(GREEN)make db-upgrade$(NC)     - Обновить базу данных (alembic upgrade head)"
  @echo "$(GREEN)make db-downgrade$(NC)   - Откатить последнюю миграцию"
  @echo "$(GREEN)make db-revision$(NC)    - Создать новую миграцию (MESSAGE='описание')"
  @echo "$(GREEN)make superuser$(NC)      - Создать суперпользователя"

venv:
  @echo "$(BLUE)Создание виртуального окружения...$(NC)"
  python -m venv .venv
  @echo "$(GREEN)Виртуальное окружение создано!$(NC)"
  @echo "Активируйте его командой: source .venv/bin/activate (Linux/Mac) или .venv\\Scripts\\activate (Windows)"

install:
  @echo "$(BLUE)Установка зависимостей...$(NC)"
  pip install --upgrade pip
  pip install -r requirements.txt
  @echo "$(GREEN)Зависимости установлены!$(NC)"

run:
  @echo "$(BLUE)Запуск приложения...$(NC)"
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
  @echo "$(BLUE)Запуск тестов...$(NC)"
  pytest -v

test-cov:
  @echo "$(BLUE)Запуск тестов с покрытием...$(NC)"
  pytest --cov=app --cov-report=html --cov-report=term

lint:
  @echo "$(BLUE)Проверка кода с помощью flake8...$(NC)"
  flake8 app/

format:
  @echo "$(BLUE)Форматирование кода...$(NC)"
  black app/
  isort app/

clean:
  @echo "$(BLUE)Очистка временных файлов...$(NC)"
  find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
  find . -type f -name "*.pyc" -delete 2>/dev/null || true
  find . -type f -name "*.pyo" -delete 2>/dev/null || true
  find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
  @echo "$(GREEN)Очистка завершена!$(NC)"

migrate: db-upgrade

db-upgrade:
  @echo "$(BLUE)Применение миграций...$(NC)"
  alembic upgrade head
  @echo "$(GREEN)Миграции применены!$(NC)"

db-downgrade:
  @echo "$(BLUE)Откат последней миграции...$(NC)"
  alembic downgrade -1
  @echo "$(GREEN)Миграция откачена!$(NC)"

db-revision:
  @echo "$(BLUE)Создание новой миграции...$(NC)"
  @if [ -z "$(MESSAGE)" ]; then \
    echo "$(RED)Ошибка: необходимо указать MESSAGE='описание'$(NC)"; \
    exit 1; \
  fi
  alembic revision --autogenerate -m "$(MESSAGE)"
  @echo "$(GREEN)Миграция создана!$(NC)"

superuser:
  @echo "$(BLUE)Создание суперпользователя...$(NC)"
  python -c "from app.core.init_superuser import create_first_superuser; import asyncio; asyncio.run(create_first_superuser())"
  @echo "$(GREEN)Суперпользователь создан!$(NC)"

db-init:
  @echo "$(BLUE)Инициализация базы данных...$(NC)"
  alembic upgrade head
  @echo "$(GREEN)База данных инициализирована!$(NC)"

setup: venv install db-init
  @echo "$(GREEN)Проект настроен! Не забудьте:$(NC)"
  @echo "1. Активировать виртуальное окружение"
  @echo "2. Создать файл .env на основе .env.example"
  @echo "3. Запустить: make run"
