import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.question_state_options import create_question_state_option, update_question_state_option, all_question_state_options, one_question_state_option
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.question_state_options import QuestionStateOptionCreate, QuestionStateOptionUpdate
from database import database
from schemes.users import UserCurrent
question_state_options_router = APIRouter(
    prefix="/question_state_options",
    tags=["Question state operation"]
)


@question_state_options_router.post('/create', )
def add_user(form: QuestionStateOptionCreate, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_question_state_option(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@question_state_options_router.get('/')
def get_question_state_options(search: str = None,  id: int = 0,question_state_id: int = 0,question_id: int = 0,  page: int = 1,
              limit: int = 25,  db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_question_state_option(db, id)

    else:
        return all_question_state_options(search=search, page=page, limit=limit, question_state_id=question_state_id, db=db,question_id=question_id )


@question_state_options_router.put("/update")
def category_update(form: QuestionStateOptionUpdate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_question_state_option(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


