import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.categories import create_category, update_category, all_categories, one_category, delete_category
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.categories import CategoryCreate, CategoryUpdate
from database import database
from schemes.users import UserCurrent
categories_router = APIRouter(
    prefix="/categories",
    tags=["Categories operation"]
)


@categories_router.post('/create', )
def add_category(form: CategoryCreate, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_category(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@categories_router.get('/')
def get_categories(search: str = None,  id: int = 0,source_id:int=None,  page: int = 1,
                   limit: int = 25, status: bool = None, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_category(db, id)
    else:
        return all_categories(search=search, page=page, limit=limit, status=status, db=db,source_id=source_id )


@categories_router.put("/update")
def category_update(form: CategoryUpdate, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_category(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@categories_router.delete("/delete")
def category_delete(id: int = 0, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_category(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
