from pydantic import(
  BaseModel,
  EmailStr,
  Field
) 
from datetime import datetime

class UserCreate(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=4)
  first_name: str = Field(..., min_length=4)
  last_name: str = Field(..., min_length=2)

class ShowUser(BaseModel):
  id: int
  email: EmailStr
  first_name: str
  last_name: str
  created_at: datetime
  updated_at: datetime | None
  
  class Config:
    from_attributes = True