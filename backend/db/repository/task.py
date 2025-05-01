from db.models.task import Task
from schemas.task import CreateTask
from schemas.task import UpdateTask
from sqlalchemy.orm import Session


def create_new_task(task: CreateTask, db: Session, user_id: int = 1):
  task = Task(**task.dict(), user_id=user_id)
  db.add(task)
  db.commit()
  db.refresh(task)
  return task


def retrieve_task(id: int, user_id: int, db: Session):
  task = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
  return task


def list_tasks(db: Session, user_id: int):
  tasks = db.query(Task).filter(Task.user_id == user_id).all()
  return tasks


def update_task(id: int, task: UpdateTask, user_id: int, db: Session):
  task_in_db = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
  if not task_in_db:
    return {"error": f"Task not found"}
  if not task_in_db.user_id == user_id:
    return {"error": f"Only the owner can modify the task"}
  task_in_db.title = task.title
  task_in_db.description = task.description
  task_in_db.is_done = task.is_done
  db.add(task_in_db)
  db.commit()
  return task_in_db


def delete_task(id: int, user_id: int, db: Session):
  task_in_db = db.query(Task).filter(Task.id == id)
  if not task_in_db.first():
    return {"error": f"Could not find task with id {id}"}
  if not task_in_db.first().user_id == user_id:
    return {"error": f"Only the owner can delete the task"}
  task_in_db.delete()
  db.commit()
  return {"msg": f"deleted task with id {id}"}
