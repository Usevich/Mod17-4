from http.client import HTTPException

# from django.contrib.sessions.models import Session
from fastapi import APIRouter, Depends, status, HTTPException
# from rest_framework import status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import Table
from sqlalchemy import insert, select, update, delete
from sqlalchemy.schema import CreateTable
from app.backend.db import Base, engine
from app.backend.db_depends import get_db
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask

router = APIRouter(
    prefix="/task",
    tags=["task"],
)

@router.get("/")
async def all_tasks(db: Annotated[Session,Depends(get_db)]):
    return db.query(Task).all()


@router.get("/{task_id}")  
async def task_by_id(task_id: int, db: Annotated[Session,Depends(get_db)]):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code = 404 , detail = "Task not found")
    return task

@router.post("/create")
async def create_task(user_id: int, task: CreateTask, db: Annotated[Session,Depends(get_db)]):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    new_task = Task()
    new_task.priority = task.priority
    new_task.user_id = task.user_id
    new_task.content = task.content
    new_task.title = task.title
    # new_task.completed = False
    new_task.slug = task.slug
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}



@router.put("/update")
async def update_task(task_id: int, task_dгata: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    task_query = db.scalar(select(Task).where(Task.id == task_id ))
    # print(user_query)
    if task_query is not None:
        db.execute(update(Task).where(Task.id == task_id).values(
            content = task_data.content,
            title = task_data.title,
            complited = True ))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update successful'}
    raise HTTPException(status_code=404, detail='Task not found')



@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task_query = db.scalar(select(Task).where(Task.id == task_id))

    if task_query is not None:
        db.delete(task_query)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete'}
    raise HTTPException(status_code=404, detail='Task not found')