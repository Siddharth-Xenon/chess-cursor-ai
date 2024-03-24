from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from .game import PyObjectId


class InsightModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    game_id: PyObjectId
    move: str
    insight_type: str  # e.g., "bad_move", "excellent_move", "book_move"
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
