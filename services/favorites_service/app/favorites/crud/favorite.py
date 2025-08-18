import asyncio
import logging
from uuid import UUID
import grpc
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import IntegrityError

from ..models import Favorite
from ..schemas import FavoriteResponse
from ...grpc_clients.auth_grpc_client import get_user_details
from ...grpc_clients.books_grpc_client import get_book_details
from ..exceptions import GrpcRetrieveDataError, ObjectDuplicateError, ObjectVerificationError, \
    ObjectCreationError, ObjectNotFoundError, UserBookFavoriteNotFoundError

class FavoriteCRUD:
    """ ==================== """
    """ Authors API Services """
    """ ==================== """
    async def add(self, db: AsyncSession, favorite: Favorite):
        """
        Create author object
        """
        try:
            logging.info(f"Request to add favorite: user_id={favorite.user_id}, book_id={favorite.book_id}")
            existing_favorite = await db.execute(
            select(Favorite).where(
                Favorite.user_id == favorite.user_id,
                Favorite.book_id == favorite.book_id
                )
            )
            if existing_favorite.scalar():
                logging.warning(f"Favorite already exis and bots: user_id={favorite.user_id}, book_id={favorite.book_id}")
                ObjectDuplicateError("Favorite", "userok")

            logging.info(f"Inserting favorite: user_id={favorite.user_id}, book_id={favorite.book_id}")
            db.add(favorite)
            await db.commit()
            logging.info(f"Favorite added: user_id={favorite.user_id}, book_id={favorite.book_id}")
            # await db.refresh(favorite)
            await asyncio.sleep(0.5)
            logging.info(f"=======crud add() Fetching user details for user_id: {favorite.user_id}")
            user_details = await get_user_details(str(favorite.user_id))
            book_details = await get_book_details(str(favorite.book_id))
            logging.info(f"=======User details fetched: {user_details}")

            if user_details is None:
                raise ObjectNotFoundError("User", favorite.user_id)
            logging.info(f"User found: {user_details}")

            if book_details is None:
                raise ObjectNotFoundError("Book", favorite.book_id)

            logging.info(f"Created new favorite.")
            return FavoriteResponse(
                id=favorite.id,
                user_id=favorite.user_id,
                book_id=favorite.book_id,
                book_details=book_details,
                user_details=user_details
            )            
        except ValidationError as e:
            logging.error(f"Failed to the favorite data verification. Error: {str(e)}")
            await db.rollback()
            raise ObjectVerificationError("Favorite", str(e))
        except grpc.RpcError as e:
            logging.error(f"Failed to fetch user details by grpc. Error: {str(e)}")
            raise GrpcRetrieveDataError(str(e))
        except grpc.aio.AioRpcError as e:
            logging.error(f"IO failed to fetch user details by grpc. Error: {str(e)}")
            raise GrpcRetrieveDataError(str(e))
        except Exception as e:
            logging.error(f"Failed to create favorite. Error: {str(e)}")
            await db.rollback()
            raise ObjectCreationError(str(e))        


    async def get_by_id(
        self, db: AsyncSession, favorite_id: UUID
    ):
        """
        Get favorite by id
        """
        try:
            statement = select(Favorite).filter(Favorite.id == favorite_id)
            result = await db.execute(statement)           
            favorite = result.scalars().one()
            logging.info(f"Retrieved favorite {favorite_id}.")
            
            book_details = await get_book_details(str(favorite.book_id))
            user_details = await get_user_details(str(favorite.user_id))
            return FavoriteResponse(
                id=favorite.id,
                user_id=favorite.user_id,
                book_id=favorite.book_id,
                book_details=book_details,
                user_details=user_details,
            )
        except NoResultFound:
            logging.warning(f"Favorite with id {favorite_id} not found.")
            raise ObjectNotFoundError("Favorite", favorite_id)
  
  
    async def get_user_favorites(self, db: AsyncSession, user_id: UUID):
        """
        Get all user favorites objects from db
        """
        statement = select(Favorite).filter(Favorite.user_id == user_id)
        result = await db.execute(statement)
        favorites = result.scalars().all()
        
        result = []
        for fav in favorites:
            book_details = await get_book_details(str(fav.book_id))
            user_details = await get_user_details(str(fav.user_id))
            result.append(FavoriteResponse(
                id=fav.id,
                user_id=fav.user_id,
                book_id=fav.book_id,
                created_at=fav.created_at,
                book_details=book_details,
                user_details=user_details,
            ))
            
        logging.info(f"Retrieved {len(favorites)} favorites.")
        return result
                  

    async def get_favorite_by_user_book(self, db: AsyncSession, user_id: str, book_id: str):
        """
        Get user favorite book object from db
        """
        try:
            statement = select(Favorite).filter(Favorite.user_id == user_id, Favorite.book_id == book_id)
            result = await db.execute(statement)           
            favorite = result.scalars().one()
            logging.info(f"Retrieved user favorite book object by user_id:{user_id} and book_id:{book_id}")
            
            book_details = await get_book_details(str(favorite.book_id))
            user_details = await get_user_details(str(favorite.user_id))
            return FavoriteResponse(
                id=favorite.id,
                user_id=favorite.user_id,
                book_id=favorite.book_id,
                book_details=book_details,
                user_details=user_details,
            )
        except NoResultFound:
            logging.warning(f"Favorite with user_id:{user_id} and book_id:{book_id} not found.")
            raise UserBookFavoriteNotFoundError("Favorite", user_id, book_id)


    async def update(
        self, db: AsyncSession, favorite_id: UUID, data
    ):
        """
        Update Favorite by id
        """
        statement = select(Favorite).filter(Favorite.id == favorite_id)

        result = await db.execute(statement)
        favorite = result.scalars().scalar_one_or_none()

        if not favorite:
            logging.warning(f"Favorite {favorite_id} not found.")
            raise ObjectNotFoundError("Favorite", favorite_id)
        
        favorite.name = data["name"]

        await db.commit()
        await db.refresh(favorite)

        logging.info(f"Successfully updated favorite {favorite_id}.")
        return favorite


    async def delete(self, db: AsyncSession, favorite_id: UUID):
        """delete favorite by id
        """
        statement = select(Favorite).filter(Favorite.id == favorite_id)
        result = await db.execute(statement)           
        favorite = result.scalars().one()
        
        if not favorite:
            raise ObjectNotFoundError("Favorite", favorite_id)
        
        await db.delete(favorite)
        await db.commit()
        await db.refresh(favorite)

        logging.info(f"Successfully deleted favorite {favorite.id}.")
        
        book_details = await get_book_details(str(favorite.book_id))
        user_details = await get_user_details(str(favorite.user_id))
        return FavoriteResponse(
            id=favorite.id,
            user_id=favorite.user_id,
            book_id=favorite.book_id,
            book_details=book_details,
            user_details=user_details,
        )
       

       
       