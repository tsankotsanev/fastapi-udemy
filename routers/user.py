from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get("/", response_model=List[UserDisplay])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return db_user.get_all_users(db)


@router.get("/{id}", response_model=UserDisplay)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return db_user.get_user(db, id)


@router.post("/{id}/update")
def update_user(
    id: int,
    request: UserBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return db_user.update_user(db, id, request)


@router.get("/delete/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return db_user.delete_user(db, id)
