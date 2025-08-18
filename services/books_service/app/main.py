import asyncio
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.grpc_server import start_grpc_server_background, stop_grpc_server_background
from .api.v1.routers import register_routes


# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application startup: Initializing gRPC server...")
    # Start the gRPC server as a background task in the main event loop
    asyncio.create_task(start_grpc_server_background())
    logging.info("Application startup: gRPC server background task initiated.")
    
    # Yield control to the application, which will handle requests
    yield
    
    # This code runs on shutdown
    logging.info("Application shutdown: Stopping gRPC server...")
    await stop_grpc_server_background()
    logging.info("Application shutdown: gRPC server stopped.")
        
tags_metadata = [
    # {
    #     "name": "Authentication", 
    #     "description": "Routes for operations related to Authentication"
    # },
    # {
    #     "name": "Book Authors",
    #     "description": "Routes for operations related to authors",
    # },
    # {
    #     "name": "Books",
    #     "description": "Routes for operations related to books",
    # },
]

app = FastAPI(
    title="Books API", 
    description="This is a simple book taking service", 
    version="0.0.1", 
    contact={
        "name": "Ali Sajadian",
        "username": "a.sajadian" 
    } ,
    license_info={
        "name": "MIT"    
    },
    docs_url="/",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# ... your other FastAPI routes and code ...
@app.get("/")
async def read_root():
    return {"message": "Auth Service REST API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[]
)

register_routes(app)

