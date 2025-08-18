import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String

from ...core.database import Base
from ...common.mixins import Timestamp
    
 
class FavoriteActionLog(Base, Timestamp):
    __tablename__ = "favorite_action_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    book_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String, nullable=False)  # e.g., "added", "removed"

       
