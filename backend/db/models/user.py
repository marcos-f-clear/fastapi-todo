from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base_class import Base

class User(Base):
  __tablename__ = "user"
  first_name: Mapped[str] = mapped_column(String(30))
  last_name: Mapped[str] = mapped_column(String(30))
  email: Mapped[str] = mapped_column(String(30), unique=True)
  password: Mapped[str] = mapped_column(String(100))
  tasks: Mapped["Task"] = relationship(back_populates="user")
  
  def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"

  def __repr__(self) -> str:
    return f"User(id={self.id!r}, name={self.full_name()!r}, email={self.email!r})"