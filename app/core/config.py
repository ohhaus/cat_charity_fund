from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot: Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
