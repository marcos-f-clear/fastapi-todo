from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class CreateTask(BaseModel):
  title: str
  description: Optional[str]
    
class UpdateTask(CreateTask):
  is_done: bool
  pass

class ShowTask(BaseModel):
  id: int
  title: str
  description: Optional[str]
  is_done: bool
  user_id: int
  created_at: datetime
  updated_at: datetime | None

  class Config:
    from_attributes = True