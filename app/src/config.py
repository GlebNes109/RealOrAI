from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # database_url: str
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_database: str
    secret_key: str
    algorithm: str
    admin_password: str
    admin_login: str
    admins: list[str]
    server_host: str
    server_port: str
    yandex_api_token: str
    database_url: str
    class Config:
        env_file = ".env"

settings = Settings()