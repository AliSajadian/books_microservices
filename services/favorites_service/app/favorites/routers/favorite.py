from http import HTTPStatus
from typing import List
from uuid import UUID
from fastapi import APIRouter, Path

from ..crud import FavoriteCRUD
from ..models import Favorite
from ..schemas.favorite import FavoriteCreate, FavoriteResponse
from ...api.dependencies.database import AsyncDbSession


""" ========================= """
""" Favorite router endpoints """
""" ========================= """
routers = APIRouter()
favorite_services = FavoriteCRUD()

@routers.post("", status_code=HTTPStatus.CREATED)
async def create_favorite(db: AsyncDbSession, favorite_data: FavoriteCreate):
    """API endpoint for creating a favorite resource

    Args:
        favorite_data (AuthorCreateModel): data for creating a favorite using the favorite schema

    Returns:
        dict: favorite that has been created
    """
    new_favorite = Favorite(
        user_id=favorite_data.user_id, 
        book_id=favorite_data.book_id
    )
    favorite = await favorite_services.add(db, new_favorite)
    return favorite


@routers.get("/user/{user_id}", response_model=List[FavoriteResponse])
async def get_user_favorites(db: AsyncDbSession, user_id: UUID):
    """API endpoint for listing all favorite resources
    """
    favorites = await favorite_services.get_user_favorites(db, user_id)
    return favorites


@routers.get("/{favorite_id}")
async def get_favorite_by_id(db: AsyncDbSession, 
    favorite_id: int = Path(..., description="The favorite id, you want to find: ", gt=0),
    # query_param: str = Query(None, max_length=5)
):
    """API endpoint for retrieving a favorite by its ID

    Args:
        favorite_id (int): the ID of the favorite to retrieve

    Returns:
        dict: The retrieved favorite
    """
    favorite = await favorite_services.get_by_id(db, favorite_id)
    return favorite


@routers.patch("/{favorite_id}")
async def update_favorite(db: AsyncDbSession, data: FavoriteCreate, 
                      favorite_id: int = Path(..., description="The favorite id, you want to update: ")):
    """Update by ID

    Args:
        favorite_id (int): ID of favorite to update
        data (AuthorCreateModel): data to update favorite

    Returns:
        dict: the updated favorite
    """
    favorite = await favorite_services.update(
        db, 
        favorite_id, 
        data={
            "user_id": data.user_id, 
            "book_id": data.book_id, 
        }
    )
    return favorite


@routers.delete("/{favorite_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_favorite(db: AsyncDbSession, favorite_id: int = Path(..., description="The favorite id, you want to delete: ")) -> None:
    """Delete favorite by id

    Args:
        favorite_id (str): ID of favorite to delete
    """
    favorite = await favorite_services.delete(db, favorite_id)
    return favorite


