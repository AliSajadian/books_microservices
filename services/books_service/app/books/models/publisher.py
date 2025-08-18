import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship 

from ...core.database import Base
from .book import Book


class BookPublisher(Base):
    __tablename__ = 'book_publishers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)


    books = relationship("Book", back_populates="publisher")
