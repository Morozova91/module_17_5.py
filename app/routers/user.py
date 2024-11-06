from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    searched_user = db.scalar(select(User).where(User.id == user_id))
    if searched_user is None:
        raise HTTPException(status_code=404, detail="User  was not found")
    return searched_user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_new_user: CreateUser):
    # Проверка на существование пользователя
    found_user = db.scalar(select(User).where(User.username == create_new_user.username))
    if found_user is not None:
        raise HTTPException(status_code=400, detail="User  with this username already exists")

    # Создание нового пользователя
    db.execute(insert(User).values(
        username=create_new_user.username,
        firstname=create_new_user.firstname,
        lastname=create_new_user.lastname,
        age=create_new_user.age,
        slug=slugify(create_new_user.username)
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{user_id}')
async def update_user(db: Annotated[Session, Depends(get_db)], updated_user: UpdateUser, user_id: int):
    # Проверка на существование пользователя
    found_user = db.scalar(select(User).where(User.id == user_id))
    if found_user is None:
        raise HTTPException(status_code=404, detail="User  not found")

    # Обновление данных пользователя
    db.execute(update(User).where(User.id == user_id).values(
        username=updated_user.username,
        firstname=updated_user.firstname,
        lastname=updated_user.lastname,
        age=updated_user.age,
        slug=slugify(updated_user.username)
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  updated successfully'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    # Проверка на существование пользователя
    found_user = db.scalar(select(User).where(User.id == user_id))
    if found_user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    # Удаление всех задач связанных с пользователем
    db.execute(delete(Task).where(Task.user_id == user_id))
    # Удаление пользователя
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  deleted successfully'}


@router.get('/{user_id}/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks