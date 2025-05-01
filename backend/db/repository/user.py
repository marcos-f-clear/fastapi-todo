from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    user = User(
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user