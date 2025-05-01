from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base_class import Base

class Task(Base):
  __tablename__ = "task"
  title: Mapped[str] = mapped_column(String(30))
  description: Mapped[Optional[str]] = mapped_column(String(255))
  user: Mapped["User"] = relationship(back_populates="tasks")
  user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
  is_done: Mapped[bool] = mapped_column(default=False)

  def __repr__(self) -> str:
      return f"Task(id={self.id!r}, title={self.title!r}, user_id={self.user_id!r})"