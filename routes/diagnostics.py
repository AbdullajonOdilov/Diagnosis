import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.diagnostics import create_diagnostics, update_diagnostics, all_diagnostics, one_diagnostics, \
    confirm_diagnostic
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.diagnostics import DiagnosticCreate, DiagnosticUpdate
from database import database
from schemes.users import UserCurrent
diagnostics_router = APIRouter(
    prefix="/diagnostics",
    tags=["Diagnostics operation"]
)


@diagnostics_router.post('/create', )
def add_diagnosis(form: DiagnosticCreate, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return create_diagnostics(form=form, thisuser=current_user, db=db)


@diagnostics_router.get('/')
def get_diagnostics(customer_id: int = 0, category_id: int = 0, id: int = 0,  page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_diagnostics(db, id)

    else:
        return all_diagnostics(category_id=category_id, customer_id=customer_id, page=page,
                               limit=limit, status=status, db=db, )


@diagnostics_router.put("/update")
def diagnosis_update(form: DiagnosticUpdate, db: Session = Depends(database),
                     current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_diagnostics(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@diagnostics_router.post("/confirm")
def diagnosis_confirm(id: int = 0, db: Session = Depends(database),
                      current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    confirm_diagnostic(id, current_user, db)
    return one_diagnostics(db, id)


