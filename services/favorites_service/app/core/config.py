from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    GRPC_AUTH_SERVICE: str
    GRPC_BOOKS_SERVICE: str

    class Config:
        env_file = ".env.docker"

settings = Settings()