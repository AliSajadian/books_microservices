from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_EXPIRE_DAYS: float
    
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_URL: str
    USER_EVENTS_EXCHANGE_NAME: str

    class Config:
        env_file = ".env.docker"

settings = Settings()