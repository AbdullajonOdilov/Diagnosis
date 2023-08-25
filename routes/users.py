import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.users import create_user, update_user, all_users, one_user, delete_user
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.users import CreateUser, UpdateUser
from database import database
from schemes.users import UserCurrent
users_router = APIRouter(
    prefix="/users",
    tags=["Users operation"]
)


@users_router.post('/create', )
def add_user(form: CreateUser, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)
             ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_user(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.get('/')
def get_users(search: str = None,  id: int = 0,  page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_user(db, id)

    else:
        return all_users(search=search, page=page, limit=limit, status=status, db=db, )


@users_router.put("/update")
def user_update(form: UpdateUser, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_user(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.delete("/delete/{id}")
def user_delete(id: int = 0, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_user(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
