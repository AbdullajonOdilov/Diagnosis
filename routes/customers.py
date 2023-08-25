import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.customers import create_customer, update_customer, all_customers, one_customer
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.customers import CustomerCreate, CustomerUpdate
from database import database
from schemes.users import UserCurrent
customers_router = APIRouter(
    prefix="/customers",
    tags=["Customers operation"]
)


@customers_router.post('/create', )
def add_user(form: CustomerCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_customer(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@customers_router.get('/')
def get_customers(search: str = None,  id: int = 0,  page: int = 1,
                  limit: int = 25, status: bool = None, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_customer(db, id)

    else:
        return all_customers(search=search, page=page, limit=limit, status=status, db=db, )


@customers_router.put("/update")
def customer_update(form: CustomerUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_customer(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


