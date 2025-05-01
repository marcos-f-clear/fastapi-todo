from typing import List
from db.session import get_db
from sqlalchemy.orm import Session
from apis.v1.auth import get_current_user
from db.models.user import User


from db.repository.task import (
  create_new_task,
  delete_task,
  list_tasks,
  retrieve_task,
  update_task,
)
from fastapi import (
  APIRouter,
  Depends,
  HTTPException,
  status,
)
from schemas.task import (
  CreateTask,
  ShowTask,
  UpdateTask
)

router = APIRouter()


@router.post("/tasks", response_model=ShowTask, status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask, current_user: User=Depends(get_current_user), db: Session = Depends(get_db)):
  task = create_new_task(task=task, db=db, user_id=current_user.id)
  return task


@router.get("/tasks/{id}", response_model=ShowTask)
def get_task(id: int, current_user: User=Depends(get_current_user), db: Session = Depends(get_db)):
  task = retrieve_task(id=id, user_id=current_user.id, db=db)
  if not task:
    raise HTTPException(
      detail=f"Task with ID {id} does not exist.",
      status_code=status.HTTP_404_NOT_FOUND,
    )
  return task


@router.get("/tasks", response_model=List[ShowTask])
def get_all_tasks(db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
  tasks = list_tasks(db=db, user_id=current_user.id)
  return tasks


@router.put("/tasks/{id}", response_model=ShowTask)
def update_a_task(id: int,  task: UpdateTask, current_user: User=Depends(get_current_user), db: Session = Depends(get_db)):
  task = update_task(id=id, task=task, user_id=current_user.id, db=db)

  if not task:
    raise HTTPException(
      detail=f"Task with id {id} does not exist",
      status_code=status.HTTP_404_NOT_FOUND,
    )
  return task


@router.delete("/tasks/{id}")
def delete_a_task(id: int, current_user: User=Depends(get_current_user), db: Session = Depends(get_db)):
  message = delete_task(id=id, user_id=current_user.id, db=db)
  if message.get("error"):
    raise HTTPException(
      detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
    )
  return {"msg": f"Successfully deleted task with id {id}"}