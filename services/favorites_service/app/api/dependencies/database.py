from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import AsyncSessionLocal#, SessionLocal


async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
        
AsyncDbSession = Annotated[AsyncSession, Depends(async_get_db)]