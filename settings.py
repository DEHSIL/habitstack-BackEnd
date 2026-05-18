from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "habitstack"
    
    # Обязательные переменные (если их нет в .env или окружении — будет ошибка)
    DATABASE_URL: str = os.getenv('DATABASE_URL')

    #JWT 
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

    # Порт автоматически преобразуется в int
    port: int = 8000

    # R2 хранилище
    R2_ENDPOINT_URL: str = os.getenv('R2_ENDPOINT_URL')
    R2_ACCESS_KEY_ID: str = os.getenv('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY: str = os.getenv('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME: str = os.getenv('R2_BUCKET_NAME')
    R2_PUBLIC_URL: str = os.getenv('R2_PUBLIC_URL')

    # Настройка для чтения из .env файла
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra='ignore'
    )

settings = Settings()