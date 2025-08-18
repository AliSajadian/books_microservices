from typing import Dict, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class FavoriteBase(BaseModel):
    user_id: UUID
    book_id: UUID

class FavoriteCreate(FavoriteBase):
    pass
    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra={
            "example":{
                "user_id":"",
                "_id":"",
            }
        }
    )
    
class FavoriteResponse(FavoriteBase):
    id: UUID
    book_details: Optional[Dict] = None
    user_details: Optional[Dict] = None

    model_config = ConfigDict(from_attributes=True)
   

    