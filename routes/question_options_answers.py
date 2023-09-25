import inspect
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.question_options_answers import create_question_options_answer, update_question_options_answer,\
    all_question_options_answers, one_question_option_answer
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.question_option_answers import QuestionOptionsAnswerCreate, QuestionOptionsAnswerUpdate
from database import database
from schemes.users import UserCurrent
question_options_answers_router = APIRouter(
    prefix="/question_options_answers",
    tags=["Question_options_answers operation"]
)


@question_options_answers_router.post('/create', )
def add_question_options_answer(form: List[QuestionOptionsAnswerCreate], db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_options_answer(form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@question_options_answers_router.get('/')
def get_question_options_answers(search: str = None,  id: int = 0,  page: int = 1,
              limit: int = 25, question_state_id: int = 0, question_option_id: int = 0, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question_option_answer(db, id)

    else:
        return all_question_options_answers(search, question_state_id, question_option_id, page=page, limit=limit,  db=db)


@question_options_answers_router.put("/update")
def question_options_answer_update(form: QuestionOptionsAnswerUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_options_answer(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


