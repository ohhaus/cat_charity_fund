# QRKot: Благотворительный фонд поддержки котиков

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.78.0-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.36-red.svg)](https://www.sqlalchemy.org/)

Сервис для сбора пожертвований на различные целевые проекты помощи котикам. Приложение позволяет создавать благотворительные проекты, принимать пожертвования от пользователей и автоматически распределять средства по проектам по принципу FIFO (First In, First Out).

## Содержание

- [Описание](#описание)
- [Функциональность](#функциональность)
- [Технологии](#технологии)
- [Установка](#установка)
- [Настройка](#настройка)
- [Использование](#использование)
- [API документация](#api-документация)
- [Структура проекта](#структура-проекта)
- [Тестирование](#тестирование)
- [Makefile команды](#makefile-команды)

## Описание

**QRKot** — это платформа для управления благотворительными проектами по поддержке котиков. Фонд может открывать несколько целевых проектов одновременно, а пользователи могут делать пожертвования, которые автоматически распределяются между открытыми проектами.

### Основные возможности:

- **Проекты**: Создание и управление целевыми благотворительными проектами
- **Пожертвования**: Прием пожертвований от пользователей с автоматическим распределением
- **Пользователи**: Регистрация, аутентификация через JWT токены
- **Автоматическое инвестирование**: Умное распределение средств по принципу FIFO

## Функциональность

### Проекты

- Каждый проект имеет название, описание и целевую сумму
- Проекты автоматически закрываются при достижении целевой суммы
- Пожертвования поступают в проекты по принципу First In, First Out
- Администраторы могут создавать, редактировать и удалять проекты

### Пожертвования

- Пользователи могут делать нецелевые пожертвования с комментариями
- Средства автоматически распределяются по открытым проектам
- При создании нового проекта неинвестированные средства автоматически в него вкладываются
- Пользователи могут просматривать свою историю пожертвований

### Права доступа

**Любой посетитель:**
- Просмотр списка всех проектов (открытых и закрытых)

**Зарегистрированный пользователь:**
- Все права посетителя
- Создание пожертвований
- Просмотр своих пожертвований

**Администратор (суперпользователь):**
- Все права зарегистрированного пользователя
- Создание проектов
- Редактирование проектов (название, описание, целевая сумма)
- Удаление проектов (только без внесенных средств)
- Просмотр всех пожертвований

## Технологии

- **Python 3.9+**
- **FastAPI** — современный веб-фреймворк для создания API
- **SQLAlchemy** — ORM для работы с базой данных
- **Alembic** — инструмент для миграций базы данных
- **Pydantic** — валидация данных
- **FastAPI Users** — управление пользователями и аутентификацией
- **SQLite/PostgreSQL** — база данных
- **Pytest** — тестирование

## Установка

### Требования

- Python 3.9 или выше
- pip
- Git

### Шаги установки

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/yourusername/cat_charity_fund.git
cd cat_charity_fund
```

2. **Создайте виртуальное окружение:**

```bash
make venv
# или вручную
python -m venv .venv
```

3. **Активируйте виртуальное окружение:**

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

4. **Установите зависимости:**

```bash
make install
# или вручную
pip install -r requirements.txt
```

## Настройка

1. **Создайте файл `.env` на основе `.env.example`:**

```bash
cp .env.example .env
```

2. **Отредактируйте `.env` файл:**

```env
# Название приложения
APP_TITLE=QRKot: Благотворительный фонд поддержки котиков

# База данных
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db

# Секретный ключ (ОБЯЗАТЕЛЬНО измените в продакшене!)
SECRET=your-super-secret-key-here

# Данные первого суперпользователя
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=secure-password
```

3. **Примените миграции базы данных:**

```bash
make migrate
# или вручную
alembic upgrade head
```

4. **Создайте суперпользователя (опционально):**

```bash
make superuser
# или вручную
python -m app.core.init_superuser
```

## Использование

### Запуск приложения

```bash
make run
# или вручную
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Интерактивная документация API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API документация

### Аутентификация

**Регистрация пользователя:**
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Вход (получение JWT токена):**
```http
POST /auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

### Проекты

**Получить список всех проектов:**
```http
GET /charity_project/
```

**Создать проект (только для администратора):**
```http
POST /charity_project/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Помощь бездомным котикам",
  "description": "Сбор средств на корм и лечение",
  "full_amount": 100000
}
```

**Обновить проект (только для администратора):**
```http
PATCH /charity_project/{project_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Новое название",
  "description": "Новое описание",
  "full_amount": 150000
}
```

**Удалить проект (только для администратора):**
```http
DELETE /charity_project/{project_id}
Authorization: Bearer <token>
```

### Пожертвования

**Создать пожертвование:**
```http
POST /donation/
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_amount": 5000,
  "comment": "На корм котикам"
}
```

**Получить свои пожертвования:**
```http
GET /donation/my
Authorization: Bearer <token>
```

**Получить все пожертвования (только для администратора):**
```http
GET /donation/
Authorization: Bearer <token>
```

## Структура проекта

```
cat_charity_fund/
├── alembic/                    # Миграции базы данных
│   └── versions/              # Файлы миграций
├── app/
│   ├── api/                   # API endpoints
│   │   ├── endpoints/         # Роутеры для различных сущностей
│   │   │   ├── auth.py       # Аутентификация
│   │   │   ├── charity_projects.py  # Проекты
│   │   │   ├── donation.py   # Пожертвования
│   │   │   └── user.py       # Пользователи
│   │   ├── routers.py        # Главный роутер
│   │   └── validators.py     # Валидаторы
│   ├── core/                  # Основные настройки
│   │   ├── config.py         # Конфигурация
│   │   ├── db.py             # Настройки базы данных
│   │   ├── user.py           # Настройки пользователей
│   │   └── init_superuser.py # Создание суперпользователя
│   ├── crud/                  # CRUD операции
│   │   ├── base.py           # Базовый CRUD
│   │   ├── charity_project.py # CRUD для проектов
│   │   └── donation.py       # CRUD для пожертвований
│   ├── models/                # Модели базы данных
│   │   ├── base_investment.py # Базовая модель для инвестиций
│   │   ├── charity_project.py # Модель проекта
│   │   ├── donation.py       # Модель пожертвования
│   │   └── user.py           # Модель пользователя
│   ├── schemas/               # Pydantic схемы
│   │   ├── charity_project.py # Схемы проекта
│   │   ├── donation.py       # Схемы пожертвования
│   │   └── user.py           # Схемы пользователя
│   ├── services/              # Бизнес-логика
│   │   └── investing.py      # Логика распределения средств
│   └── main.py               # Точка входа приложения
├── tests/                     # Тесты
├── .env.example              # Пример файла окружения
├── .gitignore
├── alembic.ini               # Конфигурация Alembic
├── Makefile                  # Команды для управления проектом
├── requirements.txt          # Зависимости Python
└── README.md                 # Этот файл
```

## Тестирование

### Запуск всех тестов:

```bash
make test
# или вручную
pytest -v
```

### Запуск тестов с покрытием кода:

```bash
make test-cov
# или вручную
pytest --cov=app --cov-report=html --cov-report=term
```

### Проверка кода с помощью flake8:

```bash
make lint
# или вручную
flake8 app/
```

## Makefile команды

Проект включает Makefile для упрощения работы:

| Команда | Описание |
|---------|----------|
| `make help` | Показать все доступные команды |
| `make venv` | Создать виртуальное окружение |
| `make install` | Установить зависимости |
| `make run` | Запустить приложение |
| `make test` | Запустить тесты |
| `make test-cov` | Запустить тесты с покрытием |
| `make lint` | Проверить код с помощью flake8 |
| `make format` | Отформатировать код (black, isort) |
| `make clean` | Очистить временные файлы |
| `make migrate` | Применить миграции |
| `make db-upgrade` | Обновить базу данных |
| `make db-downgrade` | Откатить последнюю миграцию |
| `make db-revision` | Создать новую миграцию |
| `make superuser` | Создать суперпользователя |
| `make setup` | Полная настройка проекта |

### Примеры использования:

```bash
# Полная настройка проекта с нуля
make setup

# Создать новую миграцию
make db-revision MESSAGE="Add new column"

# Запустить приложение в режиме разработки
make run

# Запустить тесты и проверить код
make test lint
```

## Безопасность

### Важные рекомендации:

1. **Никогда не используйте значения по умолчанию в продакшене!**
2. Генерируйте сложный `SECRET` ключ:
   ```bash
   openssl rand -hex 32
   ```
3. Используйте сильные пароли для суперпользователя
4. В продакшене используйте PostgreSQL вместо SQLite
5. Настройте CORS правильно для вашего фронтенда
6. Используйте HTTPS в продакшене
7. Регулярно обновляйте зависимости

## Примеры использования

### Пример работы с API через curl:

**1. Регистрация пользователя:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**2. Получение токена:**
```bash
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

**3. Создание пожертвования:**
```bash
curl -X POST "http://localhost:8000/donation/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_amount": 1000,
    "comment": "Помощь котикам"
  }'
```

## Решение проблем

### База данных не инициализируется:

```bash
# Удалите старую базу и создайте новую
rm fastapi.db
make db-init
```

### Ошибка импорта модулей:

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Переустановите зависимости
make install
```

### Тесты не проходят:

```bash
# Очистите кэш и запустите тесты заново
make clean
make test
```

## Лицензия

Этот проект создан в образовательных целях.

## Разработка

### Работа над проектом:

1. Создайте новую ветку для фичи:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Внесите изменения и проверьте код:
   ```bash
   make lint
   make test
   ```

3. Зафиксируйте изменения:
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

4. Отправьте изменения:
   ```bash
   git push origin feature/your-feature-name
   ```

### Создание новой миграции:

```bash
# После изменения моделей
make db-revision MESSAGE="Describe your changes"

# Проверьте созданную миграцию в alembic/versions/
# Примените миграцию
make db-upgrade
```

## Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для вашей фичи
3. Внесите изменения
4. Убедитесь, что все тесты проходят
5. Создайте Pull Request

## Контакты

Если у вас есть вопросы или предложения, создайте Issue в репозитории проекта.

---

**Сделано с любовью для котиков!**