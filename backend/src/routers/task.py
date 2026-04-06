from fastapi import APIRouter, Depends, HTTPException
from ..schemas import TaskCreate
from ..database import session, get_db
from ..models import Task
from ..security import auth

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/create-task")
def create_task(task: TaskCreate,db = Depends(get_db), current_user = Depends(auth.get_current_user)):
    new_task = Task(**task.model_dump(), user_id=current_user.id)    # This is a more concise way to create a new Task instance by unpacking the fields from the TaskCreate schema directly into the Task model. It eliminates the need to manually assign each field, making the code cleaner and less error-prone.
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/get-tasks")
def get_tasks(db = Depends(get_db), current_user = Depends(auth.get_current_user)):
    try:
        tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

@router.get("/get-task/{id}")
def get_task_by_id(id:int, db =Depends(get_db), current_user = Depends(auth.get_current_user)):
   task = db.query(Task).filter(Task.id == id).first()
   if task.user_id != current_user.id:
       raise HTTPException(status_code=404, detail="Not authorized to access this task")
   if not task:
       raise HTTPException(status_code=404, detail="Task not found")
   return task
       
    

@router.put("/update-task")
def update_task(id:int, task: TaskCreate, db = Depends(get_db), current_user = Depends(auth.get_current_user)):
    task_exist = db.query(Task).filter(Task.id == id).first()
    if task_exist.user_id != current_user.id:
       raise HTTPException(status_code=404, detail="Not authorized to access this task")
    if not task_exist:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump().items():    # dynamically update fields based on the provided data
        setattr(task_exist, key, value)
    # task_exist.title = task.title                 # This is the old way of updating fields, which is less flexible and more error-prone.
    # task_exist.description = task.description
    # task_exist.completed = task.completed
    db.commit()
    db.refresh(task_exist)
    return task_exist


@router.delete("/delete-task")
def delete_task(id:int, db = Depends(get_db), current_user = Depends(auth.get_current_user)):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not authorized to access this task")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}