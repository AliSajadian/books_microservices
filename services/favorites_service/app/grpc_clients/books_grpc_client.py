import logging
import asyncio
import grpc

from generated import books_pb2, books_pb2_grpc
from ..core.config import settings


# loop = asyncio.get_event_loop()  # Use the current event loop explicitly

async def get_book_details(book_id, host=settings.GRPC_BOOKS_SERVICE):
    try:
        async with grpc.aio.insecure_channel(host) as channel:
            stub = books_pb2_grpc.BooksServiceStub(channel)
            request = books_pb2.GetBookDetailsRequest(book_id=str(book_id))
            
            response = await stub.GetBookDetails(request)
            if not response:
                return None
 
            return {
                "book_id": response.book_id,
                "title": response.title,
                "author": response.author,
                "category": response.category,
                "publisher": response.publisher,
            }
    except grpc.aio.AioRpcError as e:
        logging.error(f"Error grpc fetching book details: {e}")
        return None
        # Add retry logic or return error response       
        
        