from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RABBITMQ_URL: str
    USER_EVENTS_EXCHANGE_NAME: str
    EMAIL_SERVICE_QUEUE_NAME: str
    USER_REGISTERED_ROUTING_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")


settings = Settings()

print(f"DEBUGGING CONFIG: RABBITMQ_URL = {settings.RABBITMQ_URL}")