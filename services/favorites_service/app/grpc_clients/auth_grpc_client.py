import logging
import asyncio
import grpc

from generated import auth_pb2, auth_pb2_grpc
from ..core.config import settings


# loop = asyncio.get_event_loop()  # Use the current event loop explicitly

async def get_user_details(user_id, host=settings.GRPC_AUTH_SERVICE):    
    try:
        async with grpc.aio.insecure_channel(host) as channel:
            stub = auth_pb2_grpc.AuthServiceStub(channel)
            request = auth_pb2.GetUserDetailsRequest(user_id=str(user_id))

            logging.info(f"==============get_user_details() Fetching user details for user_id: {user_id}")
            response = await stub.GetUserDetails(request)
            if not response:
                return None
            logging.info(f"==============Response fetching user details: {response}")

            return {
                "user_id": response.user_id,
                "first_name": response.first_name,
                "last_name": response.last_name,
            }
    except grpc.RpcError as e:
        logging.error(f"==============Error grpc fetching user details: {e}")
        return None
        # Add retry logic or return error response

