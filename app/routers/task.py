from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateTask, UpdateTask

from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    searched_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if searched_task is None:
        raise HTTPException(status_code=404, detail="User  was not found")
    return searched_task


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task_: CreateTask, user_id: int):
    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

    db.execute(insert(Task).values(
        title=create_task_.title,
        content=create_task_.content,
        priority=create_task_.priority,
        user_id=user_id,
        slug=slugify(create_task_.title)
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], updated_task_: UpdateTask, task_id: int):
    found_task = db.scalar(select(Task).where(Task.id == task_id))
    if found_task is None:
        raise HTTPException(status_code=404, detail="User  not found")

    # Обновление данных пользователя
    db.execute(update(Task).where(Task.id == task_id).values(
        title=updated_task_.title,
        content=updated_task_.content,
        priority=updated_task_.priority,
        user_id=updated_task_.user_id,
        slug=slugify(updated_task_.title)
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  updated successfully'}


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    found_task = db.scalar(select(Task).where(Task.id == task_id))
    if found_task is None:
        raise HTTPException(status_code=404, detail="User  not found")

    # Удаление пользователя
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  deleted successfully'}