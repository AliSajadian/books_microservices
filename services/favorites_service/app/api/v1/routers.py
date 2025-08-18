from fastapi import Depends, FastAPI
from ...favorites.routers import favorite_routers
from ..dependencies.auth_utils import verify_token


def register_routes(app: FastAPI):
    app.include_router(favorite_routers, prefix="/api/v1/favorite", tags=["User Favorite Books"], dependencies=[Depends(verify_token)])
      
# , dependencies=[Depends(verify_token)] , 

    
    