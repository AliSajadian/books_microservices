from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
# from jwt import PyJWTError
# import jwt
import logging
from jose import jwt, JWTError

from ..schemas import TokenData
from ..exceptions import AuthenticationError


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], secret_key: int, algorithm: str) -> TokenData:
    '''
    Return current user
    '''
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get('id')
        return TokenData(user_id=user_id)
    except JWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()
   
    
async def verify_token(request: Request, secret_key: int, algorithm: str):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = auth_header.split(" ")[1]
    try:
        jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    
CurrentUser = Annotated[TokenData, Depends(get_current_user)]
VerifyToken = Annotated[TokenData, Depends(verify_token)]
