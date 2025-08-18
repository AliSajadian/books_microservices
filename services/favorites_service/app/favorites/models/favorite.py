import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship 

from ...core.database import Base
from ...common.mixins import Timestamp


class Favorite(Base, Timestamp):
    __tablename__ = "favorites"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    book_id = Column(UUID(as_uuid=True), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='uq_user_book_favorite'),
    )
    