from urllib.parse import uses_query

from anyio.abc import TaskStatus
from sqlalchemy import Table
from sqlalchemy.schema import CreateTable
from app.backend.db import Base, engine
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify
router = APIRouter(
    prefix="/user", 
    tags=["user"],
)

@router.get("/")
async def all_users(db: Annotated[Session,Depends(get_db)]):
    result = db.scalars(select(User)).all()
    return result

@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id)).first()
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail='User not Found')

@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    print(user)
    print(user.username)
    new_user = User()
    new_user.username = user.username
    new_user.firstname = user.firstname
    new_user.lastname = user.lastname
    new_user.age = user.age
    db.add(new_user)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user_query = db.scalar(select(User).where(User.id == user_id ))
    print(user_query)
    # user = db.scalar(user_query).first()
    if user_query is not None:
        db.execute(update(User).where(User.id == user_id).values(
            firstname = user_data.firstname,
            lastname = user_data.lastname,
            age = user_data.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update successful'}
    raise HTTPException(status_code=404, detail='User not found')

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_query = db.scalar(select(User).where(User.id == user_id ))

    if user_query is not None:
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        for task in tasks:
            db.delete(task)
        db.delete(user_query)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete'}
    raise HTTPException(status_code=404, detail='User not found')

@router.get("/{user_id}/tasks" )
def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
  tasks = db.query(Task).filter(Task.user_id == user_id).all()
  return tasks
