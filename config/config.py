from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgresql_dsn: PostgresDsn
    debug: bool = False


app_config = Settings()
