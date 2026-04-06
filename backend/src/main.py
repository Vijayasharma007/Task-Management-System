from fastapi import FastAPI
from .routers import task, user
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from .models import Task, User


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Task Management API is running...!"}

app.include_router(task.router)
app.include_router(user.router)



# uvicorn src.main:app --reload 

