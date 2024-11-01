from sqlalchemy import Table
from sqlalchemy.schema import CreateTable
from app.backend.db import Base, engine
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify
router = APIRouter(
    prefix="/user", 
    tags=["user"],
)

@router.get("/")
async def all_users(db: Annotated[Session,Depends(get_db)]):
    result = db.scalar(select(User).all())
    return result

@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id)).first()
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail='User not Found')

@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user_query = select(User).where(User.id == user_id)
    user = db.scalar(user_query).first()
    if user is not None:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update successful'}
    raise HTTPException(status_code=404, detail='User not found')

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_query = select(User).where(User.id == user_id)
    user = db.scalar(user_query).first()
    if user is not None:
        db.delete(user)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete'}
    raise HTTPException(status_code=404, detail='User not found')
