from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.diagnostics import update_diagnositic_step
from models.categories import Categories
from models.diagnostics import Diagnostics
from models.question_options import Question_options
from models.questions import Questions
from utils.db_operations import the_one
from utils.pagination import pagination
from models.diagnostic_options import Diagnostic_options


def all_diagnostic_options(diagnostic_id, question_option_id, status, page, limit, db):
    diagnostic_options = db.query(Diagnostic_options).options(joinedload(Diagnostic_options.diagnostic),
                                                              joinedload(Diagnostic_options.question_option))

    if diagnostic_id:
        diagnostic_options = diagnostic_options.filter(Diagnostic_options.diagnostic_id == diagnostic_id)

    if question_option_id:
        diagnostic_options = diagnostic_options.filter(Diagnostic_options.question_option_id == question_option_id)

    if status in [True, False]:
        diagnostic_options = diagnostic_options.filter(Diagnostic_options.status == status)

    diagnostic_options = diagnostic_options.order_by(Diagnostic_options.id.desc())
    return pagination(diagnostic_options, page, limit)


def create_diagnostic_option(question_options_ids, form, db):
    diagnostic = the_one(db, Diagnostics, form.diagnostic_id)

    diagnostic_options_data = []
    for q_o in question_options_ids:
        question_option = the_one(db, Question_options, q_o.question_option_id)
        if db.query(Diagnostic_options).filter(Diagnostic_options.diagnostic_id == form.diagnostic_id,
                                               Diagnostic_options.question_option_id ==
                                               q_o.question_option_id).first():
            raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud")
        new_diagnostic_option_db = Diagnostic_options(
            diagnostic_id=form.diagnostic_id,
            question_option_id=q_o.question_option_id,
            question_id=question_option.question_id
        )
        diagnostic_options_data.append(new_diagnostic_option_db)
        update_diagnositic_step(id=form.diagnostic_id, question_id=question_option.question_id, db=db)

        db.add_all(diagnostic_options_data)
        db.commit()
        new_question_id = int(question_option.question_id)
        next_question = db.query(Questions).filter(Questions.category_id == diagnostic.category_id,
                                                   Questions.id > new_question_id).options(joinedload(Questions.question),

                                                joinedload(Questions.category),
                                                joinedload(Questions.question_type)).first()

        # while not next_question:
        #     new_question_id = int(question_option.question_id) + 1
        #     next_question = db.query(Questions).filter(Questions.category_id == diagnostic.category_id,
        #                                                Questions.id == new_question_id).first()
        #     print(next_question,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        print(next_question,'fffffffffffffffffffffffffffffffffffffffffffffffffff')
        return next_question


def one_diagnostic_option(db, id):
    the_item = db.query(Diagnostic_options).options(
        joinedload(Diagnostic_options.diagnostic),
        joinedload(Diagnostic_options.question_option)).filter(Diagnostic_options.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday ma'lumot mavjud emas")


def update_diagnostic_option(form, db):
    the_one(db=db, model=Diagnostic_options, id=form.id)
    the_one(db, Diagnostics, form.diagnostic_id)
    the_one(db, Question_options, form.question_options_id)
    if db.query(Diagnostic_options).filter(Diagnostic_options.diagnostic_id == form.diagnostic_id,
                                           Diagnostic_options.question_option_id ==
                                           form.question_options_id).first():
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud")
    db.query(Diagnostic_options).filter(Diagnostic_options.id == form.id).update({
        Diagnostic_options.diagnostic_id: form.diagnostic_id,
        Diagnostic_options.question_option_id: form.question_options_id
    })
    db.commit()
