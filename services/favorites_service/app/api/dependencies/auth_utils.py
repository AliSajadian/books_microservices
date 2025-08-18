from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
# from jwt import PyJWTError
# import jwt
import logging
from jose import ExpiredSignatureError, jwt, JWTError

from .schemas import TokenData
from .exceptions import AuthenticationError
from ...core.config import settings

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    '''
    Return current user
    '''
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get('id')
        return TokenData(user_id=user_id)
    except ExpiredSignatureError as e:
        logging.warning(f"Expired token: {str(e)}")
        raise HTTPException(status_code=401, detail="Expired token")
    except JWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()
   
    
async def verify_token(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        token = auth_header.split(" ")[1]
        
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError as e:
        logging.warning(f"Expired token: {str(e)}")
        raise HTTPException(status_code=401, detail="Expired token")
    except JWTError as e:
        logging.warning(f"Invalid token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
CurrentUser = Annotated[TokenData, Depends(get_current_user)]
VerifyToken = Annotated[TokenData, Depends(verify_token)]
