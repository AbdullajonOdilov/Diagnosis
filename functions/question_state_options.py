from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.question_states import Question_states
from models.questions import Questions
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.question_state_options import Question_state_options


def all_question_state_options(search, question_state_id, question_id, page, limit, db):
    question_state_options = db.query(Question_state_options).options(
        joinedload(Question_state_options.user),
        joinedload(Question_state_options.question_state))

    if search:
        search_formatted = "%{}%".format(search)
        question_state_options = question_state_options.filter(
            Question_state_options.answer.like(search_formatted) | Question_state_options.comment.like(
                search_formatted))

    if question_id:
        question_state_options = question_state_options.filter(
            Question_state_options.question_id == question_id)

    if question_state_id:
        question_state_options = question_state_options.filter(
            Question_state_options.question_state_id == question_state_id)

    question_state_options = question_state_options.order_by(Question_state_options.id.desc())
    return pagination(question_state_options, page, limit)


def create_question_state_option(form, thisuser, db):
    the_one(db, Question_states, form.question_state_id)
    the_one(db, Questions, form.question_id)
    new_question_state_db = Question_state_options(
        question_state_id=form.question_state_id,
        answer=form.answer,
        comment=form.comment,
        question_id=form.question_id,
        user_id=thisuser.id,
    )
    save_in_db(db, new_question_state_db)


def one_question_state_option(db, id):
    the_item = db.query(Question_state_options).options(joinedload(Question_state_options.user),
                                                        joinedload(Question_state_options.question),
                                                        ).filter(Question_state_options.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question_state_option mavjud emas")


def update_question_state_option(form, thisuser, db):
    the_one(db=db, model=Question_state_options, id=form.id)
    the_one(db, Question_states, form.question_state_id)
    the_one(db, Questions, form.question_id)
    db.query(Question_state_options).filter(Question_state_options.id == form.id).update({
        Question_state_options.question_state_id: form.question_state_id,
        Question_state_options.answer: form.answer,
        Question_state_options.comment: form.comment,
        Question_state_options.question_id: form.question_id,
        Question_state_options.user_id: thisuser.id,
    })
    db.commit()


