from fastapi.security import HTTPBearer
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.auth import get_user
from db.repository.user import create_new_user
from db.session import get_db
from fastapi import(
  APIRouter,
  Depends,
  HTTPException,
  status,
  Response
)
from schemas.user import(
  ShowUser,
  UserCreate
) 
from schemas.token import Token
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.repository.auth import get_user
from jose import JWTError, jwt
from fastapi.security.http import HTTPAuthorizationCredentials


router = APIRouter()


oauth2_scheme = HTTPBearer()


class LoginRequest(BaseModel):
  email: str
  password: str
  

def authenticate_user(email: str, password: str, db: Session):
  user = get_user(email=email, db=db)
  if not user:
    return False
  if not Hasher.verify_password(password, user.password):
    return False
  return user


@router.post("/auth/login", response_model=Token)
def login_for_access_token(
  login_request: LoginRequest, 
  response: Response, 
  db: Session = Depends(get_db)
):
  user = authenticate_user(login_request.email, login_request.password, db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
    )
  access_token = create_access_token(data={"sub": user.email})
  response.headers["Authorization"] = f"Bearer {access_token}"
  return {"access_token": access_token, "token_type": "bearer"}


@router.post(
  "/auth/signup", 
  response_model=Token, 
  status_code=status.HTTP_201_CREATED,
  operation_id="create_user_auth_signup"
)
def create_user(
  user: UserCreate, 
  response: Response, 
  db: Session = Depends(get_db)
):
  user = create_new_user(user=user, db=db)
  access_token = create_access_token(data={"sub": user.email})
  response.headers["Authorization"] = f"Bearer {access_token}"
  return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials"
    )

    try:
      payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
      username: str = payload.get("sub")
      
      if username is None:
        raise credentials_exception
    except JWTError as e:
      raise credentials_exception
    user = get_user(email=username, db=db)
    if user is None:
      raise credentials_exception
    return user