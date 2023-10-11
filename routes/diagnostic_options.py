import inspect
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.diagnostic_options import create_diagnostic_option, update_diagnostic_option, all_diagnostic_options, one_diagnostic_option
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.diagnostic_options import DiagnosticOptionCreate, DiagnosticOptionUpdate, QuestionOption
from database import database
from schemes.users import UserCurrent
diagnostic_options_router = APIRouter(
    prefix="/diagnostic_options",
    tags=["Diagnostic_options operation"]
)


@diagnostic_options_router.post('/create', )
def add_diagnostic_options(question_option_ids: List[QuestionOption], form: DiagnosticOptionCreate,
                           db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return create_diagnostic_option(question_option_ids, form=form, db=db)



@diagnostic_options_router.get('/')
def get_diagnostic_options(diagnostic_id: int = 0, question_options_id: int = 0,  id: int = 0,  page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_diagnostic_option(db, id)

    else:
        return all_diagnostic_options(diagnostic_id=diagnostic_id, question_option_id=question_options_id,
                                      page=page, limit=limit, status=status, db=db, )


@diagnostic_options_router.put("/update")
def diagnostic_optionsupdate(form: DiagnosticOptionUpdate, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_diagnostic_option(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


