import logging
import asyncio
from concurrent import futures
import grpc
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID # Needed for UUID conversion

from generated import books_pb2, books_pb2_grpc
from app.books.models import Book
from app.core.database import AsyncSessionLocal

# Configure logging (ensure this is at the top level of the file)
logging.basicConfig(level=logging.ERROR, format='%(levelname)s:%(name)s:%(message)s')
# If you want to see INFO and DEBUG from SQLAlchemy, uncomment this:
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

_grpc_server_instance = None

async def start_grpc_server_background():
    """
    Starts the gRPC server in the background as an asyncio task.
    """
    global _grpc_server_instance
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BooksServiceServicer_to_server(BooksServiceServicer(), server)

    listen_addr = '[::]:50052' # Ensure this is the correct gRPC port for your setup
    server.add_insecure_port(listen_addr)
    logging.info(f"gRPC server starting as a background task on {listen_addr}")

    await server.start()
    _grpc_server_instance = server # Store the server instance for graceful shutdown

async def stop_grpc_server_background():
    """
    Stops the gRPC server gracefully.
    """
    global _grpc_server_instance
    if _grpc_server_instance:
        logging.info("gRPC server stopping...")
        await _grpc_server_instance.stop(grace=5) # Graceful shutdown with 5 seconds grace period
        _grpc_server_instance = None
        logging.info("gRPC server stopped.")


class BooksServiceServicer(books_pb2_grpc.BooksServiceServicer):
    async def GetBookDetails(self, request: books_pb2.GetBookDetailsRequest, context: grpc.aio.ServicerContext):
        # Assuming your .proto defines a message like:
        # message GetBookDetailsRequest {
        #   string book_id = 1;
        # }
        # If your message is named differently (e.g., BookDetailsRequest), adjust the type hint above.

        try:
            # We are fetching book details, so we expect a book_id in the request.
            # The 'user_id = request.user_id' line was incorrect and has been removed.
            book_id_str = request.book_id
            logging.error(f"DEBUG: Received Book ID (string): {book_id_str}")
            logging.error(f"DEBUG: Type of received Book ID: {type(book_id_str)}")

            try:
                book_id_uuid = UUID(book_id_str)
                logging.error(f"DEBUG: Converted Book ID (UUID): {book_id_uuid}")
                logging.error(f"DEBUG: Type of converted Book ID: {type(book_id_uuid)}")
            except ValueError as ve:
                logging.error(f"ERROR: Invalid UUID format received for book_id: {book_id_str} - {ve}")
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid book ID format.")
                return # Important: return after aborting context

            async with AsyncSessionLocal() as session:
                logging.error(f"DEBUG: GetBookDetails - Current Loop (inside DB session): {asyncio.get_running_loop()}")

                result = await session.execute(
                    select(Book)
                    .options(
                        selectinload(Book.author),
                        selectinload(Book.category),
                        selectinload(Book.publisher),
                    )
                    .where(Book.id == book_id_uuid) # Use the converted UUID
                )
                book = result.scalar_one_or_none()

                if not book:
                    logging.error(f"DEBUG: Book with ID {book_id_str} not found in database.")
                    await context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")
                    return # Important: return after aborting context

                # Safe: access everything you need INSIDE the session context before returning
                author_name = book.author.name if book.author else None
                category_name = book.category.name if book.category else None
                publisher_name = book.publisher.name if book.publisher else None

                return books_pb2.BookDetailsResponse(
                    book_id=str(book.id),
                    title=book.title,
                    author=author_name,
                    category=category_name,
                    publisher=publisher_name,
                )

        except Exception as e:
            # Use logging.exception to print the full traceback for better debugging
            logging.exception(f"DEBUG: An unexpected error occurred while fetching book details: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, "Internal error occurred")
            return # Important: return after aborting context