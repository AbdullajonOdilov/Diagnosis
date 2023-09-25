import inspect
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.question_options import create_question_option, update_question_option, all_question_options, \
    one_question_option
from functions.questions import one_question
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.question_options import QuestionOptionUpdate, Answer, QuestionOptionCreate
from database import database
from schemes.users import UserCurrent
question_options_router = APIRouter(
    prefix="/question_options",
    tags=["Question_options operation"]
)


@question_options_router.post('/create', )
def add_q_o(answers: List[Answer], form: QuestionOptionCreate, db: Session = Depends(database),
            current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_option(answers, form, thisuser=current_user, db=db)
    return one_question(db, form.question_id)


@question_options_router.get('/')
def get_question_options(search: str = None, id: int = 0, question_id: int = 0,  page: int = 1,
                         limit: int = 25,  db: Session = Depends(database),
                         current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question_option(db, id)
    else:
        return all_question_options(search=search, page=page, limit=limit, db=db, question_id=question_id)


@question_options_router.put("/update")
def question_option_update(form: QuestionOptionUpdate, db: Session = Depends(database),
                           current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_option(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


