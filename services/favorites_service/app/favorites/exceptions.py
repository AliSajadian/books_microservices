from fastapi import HTTPException

class ObjectError(HTTPException):
    """Base exception for favorite-related errors"""
    pass

class ObjectNotFoundError(ObjectError):
    def __init__(self, name: str, onject_id=None):
        message = f"{name} not found" if onject_id is None else f"{name} with id {onject_id} not found"
        super().__init__(status_code=404, detail=message)


class UserBookFavoriteNotFoundError(ObjectError):
    def __init__(self, name: str, user_id=None, book_id=None):
        message = f"{name} with user_id:{user_id} and book_id:{book_id} not found." 
        super().__init__(status_code=404, detail=message)


class ObjectDuplicateError(ObjectError):
    def __init__(self, name: str, item: str):
        message = f"{name} already exists for this {item}." 
        super().__init__(status_code=409, detail=message)


class ObjectCreationError(ObjectError):
    def __init__(self, error: str):
        super().__init__(status_code=409, detail=["the request could not be completed due to a conflict with the current state of the target resource.", f"Error: {error}"])


class ObjectVerificationError(ObjectError):
    def __init__(self, name: str, error: str):
        super().__init__(status_code=422, detail=f"Failed to the {name} data verification: {error}")
        
        
class GrpcRetrieveDataError(ObjectError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to fetch user details by grpc. Error: {error}") 



