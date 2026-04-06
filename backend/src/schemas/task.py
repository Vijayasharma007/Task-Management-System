# Schemas define what data looks like — what you send in and get back from your API.
# This is where you define the structure of your data, including types and validation rules.

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str = None # Optional field
    completed: bool = False