from apis.router import api_router
from db.base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_tables():
  Base.metadata.create_all(bind=engine)

def include_router(app):
  app.include_router(api_router)

def start_application():
  app = FastAPI()
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization", "authorization"],
  )
  create_tables()
  include_router(app)
  return app

app = start_application()

@app.get("/")
def root():
    return {"msg": "Up and running!"}