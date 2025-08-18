import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship 

from ...core.database import Base
from ...common.mixins import Timestamp


class FavoriteCollection(Base, Timestamp):
    __tablename__ = "favorite_collections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_collection_name'),
    )


  
    
