from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot: Благотворительный фонд поддержки котиков'
    app_description: str = (
        'Сервис для сбора пожертвований на различные целевые проекты'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: str = 'root@admin.ru'
    first_superuser_password: str = 'root'

    class Config:
        env_file = '.env'


settings = Settings()
