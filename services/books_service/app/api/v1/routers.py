from fastapi import Depends, FastAPI
from ...books.routers import author_routers, book_routers, category_routers, publisher_routers
from ..dependencies.auth_utils import verify_token


def register_routes(app: FastAPI):
    app.include_router(author_routers, prefix="/api/v1/author", tags=["Book Authors"], dependencies=[Depends(verify_token)])
    app.include_router(category_routers, prefix="/api/v1/category", tags=["Book Categories"])
    app.include_router(publisher_routers, prefix="/api/v1/publisher", tags=["Book Publishers"])
    app.include_router(book_routers, prefix="/api/v1/book", tags=["Books"])
    
    
# , dependencies=[Depends(verify_token)] , 

    
    