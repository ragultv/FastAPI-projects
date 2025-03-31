from fastapi import FastAPI, Depends, HTTPException
import models, schema
from database import engine, sessionLOCAL, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLOCAL()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks", response_model=schema.Taskresponse)
def create_task(task: schema.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=list[schema.Taskresponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.task).all()
    return tasks

@app.put("/tasks/{task_id}", response_model=schema.Taskresponse)  # ✅ Fixed
def update_task(task_id: int, task_update: schema.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.task).filter(models.task.id == task_id).first()
    if task is None:  # ✅ Fixed
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.task).filter(models.task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}  # ✅ Fixed JSON response
