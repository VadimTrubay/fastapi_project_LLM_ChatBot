from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    """Configuration settings for the application."""
    postgres_db: str = 'test'
    postgres_user: str = 'test'
    postgres_password: str = 'test'
    postgres_port: int = 5432
    postgres_host: str = 'test'
    sqlalchemy_database_url: str = 'postgresql+psycopg2://user:password@localhost:5432/postgres'
    secret_key: str = 'test'
    algorithm: str = 'test'
    mail_username: str = 'test'
    mail_password: str = 'test'
    mail_from: str = 'test'
    mail_port: int = 465
    mail_server: str = 'test'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = "test"
    cloudinary_name: str = 'test'
    cloudinary_api_key: str = 'test'
    cloudinary_api_secret: str = 'test'
    openai_api_key: str = 'key'
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

    # class Config:
    #     env_file = Path(__file__).parent.joinpath(".env")
    #     env_file_encoding = "utf-8"


settings = Settings()

# print(settings.sqlalchemy_database_url)