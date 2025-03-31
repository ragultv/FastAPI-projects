from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class TaskCreate(TaskBase):  # Does NOT include `id`
    pass

class Taskresponse(TaskBase):  # Response includes `id`
    id: int

    class Config:  # Fixed capitalization
        orm_mode = True  # Ensures compatibility with SQLAlchemy models
