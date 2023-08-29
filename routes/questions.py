import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.questions import create_question, update_question, all_questions, one_question
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.questions import QuestionCreate, QuestionUpdate
from database import database
from schemes.users import UserCurrent
questions_router = APIRouter(
    prefix="/questions",
    tags=["Question operation"]
)


@questions_router.post('/create')
def add_question(form: QuestionCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@questions_router.get('/')
def get_questions(search: str = None,  id: int = 0, category_id: int = 0, question_type_id: int = 0,  page: int = 1,
              limit: int = 25,   db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question(db, id)

    else:
        return all_questions(search=search, page=page, limit=limit,  db=db,
                             category_id=category_id,question_type_id=question_type_id )


@questions_router.put("/update")
def question_update(form: QuestionUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


