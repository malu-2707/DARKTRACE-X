from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Autonomous SOC Agent"
    app_env: str = "development"
    debug: bool = True

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    database_url: str = "sqlite:///./alerts.db"

    jwt_secret: str = "CHANGE_THIS_SECRET"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()