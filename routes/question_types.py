import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.question_types import create_question_type, update_question_type, all_question_types, one_question_type
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.question_types import QuestionTypeCreate, QuestionTypeUpdate
from database import database
from schemes.users import UserCurrent
question_types_router = APIRouter(
    prefix="/question_types",
    tags=["Question_types operation"]
)


@question_types_router.post('/create', )
def add_question_type(form: QuestionTypeCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_type(form=form, thisuser=current_user,  db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@question_types_router.get('/')
def get_question_types(search: str = None,  id: int = 0,  page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question_type(db, id)

    else:
        return all_question_types(search=search, page=page, limit=limit, status=status, db=db, )


@question_types_router.put("/update")
def question_type_update(form: QuestionTypeUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_type(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


