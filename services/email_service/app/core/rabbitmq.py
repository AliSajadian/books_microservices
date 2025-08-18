import asyncio
import json
import logging
from typing import Callable, Optional
import aio_pika
from aio_pika import Connection, Channel, IncomingMessage

from app.core.config import settings

logger = logging.getLogger(__name__)

_rabbitmq_connection: Optional[Connection] = None
_rabbitmq_channel: Optional[Channel] = None
_consumer_task: Optional[asyncio.Task] = None

async def connect_and_start_consuming(process_message_callback: Callable[[dict], None]):
    """Establishes connection, declares queue, and starts consuming messages."""
    global _rabbitmq_connection, _rabbitmq_channel, _consumer_task
    try:
        logger.info(f"Attempting to connect to RabbitMQ at {settings.RABBITMQ_URL}...")
        print(f"DEBUGGING RABBITMQ: Connecting with URL: {settings.RABBITMQ_URL}")
        _rabbitmq_connection = await aio_pika.connect_robust(
            settings.RABBITMQ_URL,
            loop=asyncio.get_event_loop()
        )
        _rabbitmq_channel = await _rabbitmq_connection.channel()
        logger.info("RabbitMQ connection and channel established for consumer.")

        # Declare the exchange (ensure it exists and type matches producer)
        exchange = await _rabbitmq_channel.declare_exchange(
            settings.USER_EVENTS_EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True
        )

        # Declare a queue for the email service
        queue = await _rabbitmq_channel.declare_queue(
            settings.EMAIL_SERVICE_QUEUE_NAME, durable=True
        )
        logger.info(f"Queue '{settings.EMAIL_SERVICE_QUEUE_NAME}' declared.")

        # Bind the queue to the exchange with the specific routing key
        await queue.bind(exchange, routing_key=settings.USER_REGISTERED_ROUTING_KEY)
        logger.info(f"Queue '{settings.EMAIL_SERVICE_QUEUE_NAME}' bound to '{settings.USER_EVENTS_EXCHANGE_NAME}' with routing key '{settings.USER_REGISTERED_ROUTING_KEY}'.")

        async def on_message(message: IncomingMessage):
            async with message.process():
                try:
                    message_data = message.body.decode('utf-8')
                    event = json.loads(message_data)
                    logger.info(f"Received message: {event}")
                    await process_message_callback(event) # Call the provided callback
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode JSON message: {message.body}")
                except Exception as e:
                    logger.exception(f"Error processing message: {e}")

        # Start consuming messages in a separate task
        _consumer_task = asyncio.create_task(queue.consume(on_message))
        logger.info("Started consuming messages.")

    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ or start consuming: {e}")
        # In a real app, implement robust retry logic.

async def disconnect_rabbitmq():
    """Closes the RabbitMQ connection and cancels the consumer task."""
    global _rabbitmq_connection, _rabbitmq_channel, _consumer_task
    if _consumer_task:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            logger.info("RabbitMQ consumer task cancelled.")
    
    if _rabbitmq_channel and not _rabbitmq_channel.is_closed:
        await _rabbitmq_channel.close()
        logger.info("RabbitMQ channel closed.")
    if _rabbitmq_connection and not _rabbitmq_connection.is_closed:
        await _rabbitmq_connection.close()
        logger.info("RabbitMQ connection closed.")