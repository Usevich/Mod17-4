from pydantic import BaseModel
from sqlalchemy import Boolean


class CreateUser(BaseModel):
    username: str
    firstname: str 
    lastname: str
    age: int

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class CreateTask(BaseModel): 
    priority: int
    user_id: int
    content: str
    title: str
    complited : bool
    slug: str

class UpdateTask(BaseModel):
    title: str
    content: str 
    priority: int