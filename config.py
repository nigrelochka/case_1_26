from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  # ХРАНИТ ОСНОВНЫЕ НАСТРОЙКИ ПРИЛОЖЕНИЯ.
  appName: str = Field(default='Text Analyzer', validation_alias='APP_NAME')
  appHost: str = Field(default='127.0.0.1', validation_alias='APP_HOST')
  appPort: int = Field(default=8000, validation_alias='APP_PORT')
  redisHost: str = Field(default='localhost', validation_alias='REDIS_HOST')
  redisPort: int = Field(default=6379, validation_alias='REDIS_PORT')

  model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
