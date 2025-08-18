import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.rabbitmq import connect_and_start_consuming, disconnect_rabbitmq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_welcome_email(user_id: str, email: str, username: str):
    """
    Simulates sending a welcome email.
    In a real application, this would integrate with an actual email sending service
    (e.g., SMTP, SendGrid, Mailgun).
    """
    logger.info(f"--- SIMULATING EMAIL SEND ---")
    logger.info(f"To: {email}")
    logger.info(f"Subject: Welcome to Our Service, {username}!")
    logger.info(f"Body: Hello {username}, thank you for registering with user ID {user_id}. We hope you enjoy our services!")
    logger.info(f"-----------------------------")
    await asyncio.sleep(1) # Simulate network delay


async def process_user_event(event: dict):
    """Callback function to process incoming user events from RabbitMQ."""
    event_type = event.get("event_type")
    if event_type == "UserRegistered":
        user_id = event.get("user_id")
        email = event.get("email")
        username = event.get("username")
        logger.info(f"Processing 'UserRegistered' event for user: {username} ({user_id})")
        await send_welcome_email(user_id, email, username)
    else:
        logger.warning(f"Unknown event type received: {event_type}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up email_service...")
    # Start the RabbitMQ consumer when the app starts
    await connect_and_start_consuming(process_user_event)
    logger.info("Email service consumer started.")
    yield
    logger.info("Shutting down email_service...")
    # Disconnect RabbitMQ when the app shuts down
    await disconnect_rabbitmq()
    logger.info("Email service shutdown complete.")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "email_service"}