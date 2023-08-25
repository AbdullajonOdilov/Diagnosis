import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.categories import create_category, update_category, all_categories, one_category
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.categories import CategoryCreate, CustomerUpdate
from database import database
from schemes.users import UserCurrent
categories_router = APIRouter(
    prefix="/categories",
    tags=["Categories operation"]
)


@categories_router.post('/create', )
def add_user(form: CategoryCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_category(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@categories_router.get('/')
def get_categories(search: str = None,  id: int = 0,  page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_category(db, id)

    else:
        return all_categories(search=search, page=page, limit=limit, status=status, db=db, )


@categories_router.put("/update")
def category_update(form: CustomerUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_category(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


