import asyncio

try:
    from app.core.init_superuser import create_superuser
except (ImportError, NameError):
    raise ImportError(
        'Не удалось импортировать функцию `create_user` из модуля '
        '`app.core.init_db`. Создайте суперпользователя самостоятельно.'
    )


class UserCreationError(Exception):
    pass


if __name__ == '__main__':
    try:
        asyncio.run(create_superuser())
    except Exception:
        raise UserCreationError(
            'Не удалось создать суперпользователя. '
            'Создайте суперпользователя самостоятельно:\n'
            'email: root@admin.ru\n'
            'password: root'
        )
