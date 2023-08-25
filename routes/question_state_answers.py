import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.question_state_answers import create_question_state_answer, update_question_state_answer, all_question_state_answers, one_question_state_answer
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.question_state_answers import QuestionStateAnswerCreate, QuestionStateAnswerUpdate
from database import database
from schemes.users import UserCurrent
question_state_answers_router = APIRouter(
    prefix="/question_state_answers",
    tags=["Question_state_answers operation"]
)


@question_state_answers_router.post('/create', )
def add_user(form: QuestionStateAnswerCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_state_answer(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@question_state_answers_router.get('/')
def get_question_state_answers(search: str = None,  id: int = 0,  page: int = 1,
              limit: int = 25, question_state_option_id: int = 0, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question_state_answer(db, id)

    else:
        return all_question_state_answers(search=search, page=page, limit=limit,   db=db,question_state_option_id=question_state_option_id )


@question_state_answers_router.put("/update")
def category_update(form: QuestionStateAnswerUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_state_answer(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


