import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, UniqueConstraint

from ...core.database import Base
from ...common.mixins import Timestamp


class FavoriteCollectionItem(Base, Timestamp):
    __tablename__ = "favorite_collection_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("favorite_collections.id"), nullable=False) 
    book_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (
        UniqueConstraint('collection_id', 'book_id', name='uq_collection_book'),
    )