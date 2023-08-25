import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.question_states import create_question_state, update_question_state, all_question_states, one_question_state
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.question_states import QuestionStateCreate, QuestionStateUpdate
from database import database
from schemes.users import UserCurrent
question_states_router = APIRouter(
    prefix="/question_states",
    tags=["Question_states operation"]
)


@question_states_router.post('/create', )
def add_user(form: QuestionStateCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_state(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@question_states_router.get('/')
def get_question_states(search: str = None,  id: int = 0,  page: int = 1,
              limit: int = 25,   db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question_state(db, id)

    else:
        return all_question_states(search=search, page=page, limit=limit,   db=db, )


@question_states_router.put("/update")
def question_state_update(form: QuestionStateUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_state(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


