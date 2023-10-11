import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.customers import Customers
from models.diagnostic_options import Diagnostic_options
from models.question_options import Question_options
from models.question_options_answers import Question_options_answers
from models.questions import Questions
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.diagnostics import Diagnostics


def all_diagnostics(customer_id, category_id, status, page, limit, db):
    diagnostics = db.query(Diagnostics).options(joinedload(Diagnostics.user),
                                                joinedload(Diagnostics.customer),
                                                joinedload(Diagnostics.category))

    if customer_id:
        diagnostics = diagnostics.filter(Diagnostics.customer_id == customer_id)
    if category_id:
        diagnostics = diagnostics.filter(Diagnostics.category_id == category_id)
    if status in [True, False]:
        diagnostics = diagnostics.filter(Diagnostics.status == status)

    diagnostics = diagnostics.order_by(Diagnostics.id.desc())
    return pagination(diagnostics, page, limit)


def create_diagnostics(form, thisuser, db):
    the_one(db, Customers, form.customer_id)
    the_one(db, Categories, form.category_id)
    diagnosis = db.query(Diagnostics).filter(Diagnostics.category_id == form.category_id,
                                             Diagnostics.customer_id == form.customer_id).first()
    if diagnosis:
        raise HTTPException(status_code=400, detail="Bu mijoz bu categoriyaga biriktirilgan")
    new_diagnostics_db = Diagnostics(
        customer_id=form.customer_id,
        category_id=form.category_id,
        date=datetime.date.today(),
        status=False,
        user_id=thisuser.id,
    )
    save_in_db(db, new_diagnostics_db)

    return {"customer_id": form.customer_id, "category_id": form.category_id,
            "status": False}


def one_diagnostics(db, id):
    the_one(db, Diagnostics, id)
    the_item = db.query(Diagnostics) \
        .filter(Diagnostics.id == id) \
        .options(
        joinedload(Diagnostics.user),
        joinedload(Diagnostics.customer),
        joinedload(Diagnostics.category)
            .subqueryload(Categories.category_question)
            .options(
            joinedload(Questions.question_type),
            joinedload(Questions.diagnosis_option_question)
                .subqueryload(Diagnostic_options.question_option)
                .options(
                joinedload(Question_options.question_options_answer)
                    .subqueryload(Question_options_answers.question_state)
            )
        )
    ) \
        .first()

    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday diagnostics mavjud emas")


def update_diagnostics(form, thisuser, db):
    diagnos = the_one(db=db, model=Diagnostics, id=form.id)
    the_one(db, Customers, form.customer_id)
    the_one(db, Categories, form.category_id)
    diagnosis = db.query(Diagnostics).filter(Diagnostics.category_id == form.category_id,
                                             Diagnostics.customer_id == form.customer_id).first()

    if diagnosis and diagnos.category_id != form.category_id:
        raise HTTPException(status_code=400, detail="Bu mijoz bu categoriyaga biriktirilgan")

    if diagnos.status == True:
        raise HTTPException(status_code=400, detail="Bu diagnos tugagan")

    db.query(Diagnostics).filter(Diagnostics.id == form.id).update({
        Diagnostics.customer_id: form.customer_id,
        Diagnostics.category_id: form.category_id,
        Diagnostics.date: datetime.date.today(),
        Diagnostics.user_id: thisuser.id,
    })
    db.commit()


def confirm_diagnostic(id, thisuser, db):
    the_one(db=db, model=Diagnostics, id=id)
    db.query(Diagnostics).filter(Diagnostics.id == id).update({
        Diagnostics.status: True,
        Diagnostics.user_id: thisuser.id,
    })
    db.commit()


def update_diagnositic_step(id, question_id, db):
    db.query(Diagnostics).filter(Diagnostics.id == id).update({
        Diagnostics.step: question_id
    })
    db.commit()
