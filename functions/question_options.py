from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.questions import Questions
from utils.db_operations import the_one
from utils.pagination import pagination
from models.question_options import Question_options


def all_question_options(search, question_id, page, limit, db):
    question_options = db.query(Question_options).options(joinedload(Question_options.question),
                                                          joinedload(Question_options.question_options_answer))

    if search:
        search_formatted = "%{}%".format(search)
        question_options = question_options.filter(
            Question_options.answer.like(search_formatted) | Question_options.comment.like(
                search_formatted))

    if question_id:
        question_options = question_options.filter(
            Question_options.question_id == question_id)

    question_options = question_options.order_by(Question_options.id.desc())
    return pagination(question_options, page, limit)


def create_question_option(answers, form, thisuser, db):
    the_one(db, Questions, form.question_id)
    question_options_data = []
    for answer in answers:
        qso_ver = db.query(Question_options).filter(Question_options.question_id == form.question_id,
                                                    Question_options.answer == answer.answer).first()
        if qso_ver:
            raise HTTPException(status_code=400, detail="Bu javob bu savol uchun allaqachon biriktirilgan")
        new_question_state_db = Question_options(
            question_id=form.question_id,
            answer=answer.answer,
            comment=form.comment,
            user_id=thisuser.id,
        )
        question_options_data.append(new_question_state_db)

    db.add_all(question_options_data)
    db.commit()


def one_question_option(db, id):
    the_item = db.query(Question_options).options(joinedload(Question_options.question)
                                                        ).filter(Question_options.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question_state_option mavjud emas")


def update_question_option(form, thisuser, db):
    qso = the_one(db=db, model=Question_options, id=form.id)
    the_one(db, Questions, form.question_id)

    qso_ver = db.query(Question_options).filter(Question_options.question_id == form.question_id,
                                                Question_options.answer == form.answer).first()
    if qso_ver and qso.answers != form.answer:
        raise HTTPException(status_code=400, detail="Bu javob bu savol uchun allaqachon biriktirilgan")

    db.query(Question_options).filter(Question_options.id == form.id).update({
        Question_options.answer: form.answer,
        Question_options.comment: form.comment,
        Question_options.question_id: form.question_id,
        Question_options.user_id: thisuser.id,
    })
    db.commit()


