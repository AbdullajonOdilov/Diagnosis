from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.diagnostic_options import Diagnostic_options


def all_diagnostic_options(diagnostic_id, question_state_option_id, status, page, limit, db):
    diagnostic_options = db.query(Diagnostic_options).options(joinedload(Diagnostic_options.user), joinedload(Diagnostic_options.customer, ),
                                                joinedload(Diagnostic_options.category, )
                                                )

    if diagnostic_id:
        diagnostic_options = diagnostic_options.filter(Diagnostic_options.diagnostic_id == diagnostic_id)

    else:
        diagnostic_options = diagnostic_options
    if question_state_option_id:
        diagnostic_options = diagnostic_options.filter(Diagnostic_options.question_state_option_id == question_state_option_id)
    else:
        diagnostic_options = diagnostic_options

    if status in [True, False]:
        diagnostic_options = diagnostic_options.filter(Diagnostic_options.status == status)
    else:
        diagnostic_options = diagnostic_options

    diagnostic_options = diagnostic_options.order_by(Diagnostic_options.id.desc())
    return pagination(diagnostic_options, page, limit)


def create_diagnostic_option(form, db, thisuser):
    new_diagnostic_option_db = Diagnostic_options(
        diagnostic_id=form.diagnostic_id,
        question_state_option_id=form.question_state_option_id,
        user_id=thisuser.id,
    )

    save_in_db(db=Diagnostic_options, obj=new_diagnostic_option_db)

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_diagnostic_option(db, id):
    the_item = db.query(Diagnostic_options).options(joinedload(Diagnostic_options.user), joinedload(Diagnostic_options.customer, ),
                                             joinedload(Diagnostic_options.category, )).filter(
        Diagnostic_options.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday diagnostic_option mavjud emas")


def update_diagnostic_option(form, thisuser, db):
    the_one(db=db, model=Diagnostic_options, id=form.id)

    db.query(Diagnostic_options).filter(Diagnostic_options.id == form.id).update({
        Diagnostic_options.diagnostic_id: form.diagnostic_id,
        Diagnostic_options.question_state_option_id: form.question_state_option_id,
        Diagnostic_options.user_id: thisuser.id,

    })

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")

