from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_URL: str
    USER_EVENTS_EXCHANGE_NAME: str
    EMAIL_SERVICE_QUEUE_NAME: str
    USER_REGISTERED_ROUTING_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")

    @property
    def rabbitmq_url(self):
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

settings = Settings()

print(f"DEBUGGING CONFIG: RABBITMQ_URL = {settings.RABBITMQ_URL}")