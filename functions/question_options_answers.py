from fastapi import HTTPException
from sqlalchemy.orm import joinedload, subqueryload

from models.question_options import Question_options
from models.question_states import Question_states
from utils.db_operations import the_one
from utils.pagination import pagination
from models.question_options_answers import Question_options_answers


def all_question_options_answers(search, question_id, question_state_id, question_option_id,  page, limit, db):
    question_options_answers = db.query(Question_options_answers).join(Question_options_answers.question_option).options(
        joinedload(Question_options_answers.question_state),
        joinedload(Question_options_answers.question_option).options(subqueryload(Question_options.question)))

    if question_id:
        question_options_answers = question_options_answers.\
            filter(Question_options.question_id == question_id)
    if search:
        search_formatted = "%{}%".format(search)
        question_options_answers = question_options_answers.filter(Question_options_answers.answer.like(search_formatted)
                                                               | Question_options_answers.comment.like(search_formatted))
    if question_state_id:
        question_options_answers = question_options_answers.\
            filter(Question_options_answers.question_state_id == question_state_id)

    if question_option_id:
        question_options_answers = question_options_answers.\
            filter(Question_options_answers.question_option_id == question_option_id)

    question_options_answers = question_options_answers.order_by(Question_options_answers.id.desc())
    return pagination(question_options_answers, page, limit)


def one_question_option_answer(db, id):
    the_item = db.query(Question_options_answers).join(Question_options_answers.question_option).options(
        joinedload(Question_options_answers.question_state),
        joinedload(Question_options_answers.question_option).options(subqueryload(Question_options.question)))\
        .filter(Question_options_answers.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question_state mavjud emas")


def create_question_options_answer(form, thisuser, db):

    question_options_answer_date = []
    for item in form:
        the_one(db, Question_options, item.question_option_id)
        the_one(db, Question_states, item.question_state_id)
        if db.query(Question_options_answers).filter(Question_options_answers.question_state_id == item.question_state_id,
                                                     Question_options_answers.question_option_id == item.question_option_id,
                                                     Question_options_answers.answer == item.answer).first():
            raise HTTPException(status_code=400, detail="Bu javob bu holat option uchn mavjud")
        new_question_o_a_db = Question_options_answers(
            question_state_id=item.question_state_id,
            question_option_id=item.question_option_id,
            answer=item.answer,
            comment=item.comment,
            user_id=thisuser.id,
        )
        question_options_answer_date.append(new_question_o_a_db)

    db.add_all(question_options_answer_date)
    db.commit()


def update_question_options_answer(form, thisuser, db):
    qoa = the_one(db=db, model=Question_options_answers, id=form.id)
    the_one(db, Question_states, form.question_state_id)
    the_one(db, Question_options, form.question_option_id)
    qoa_ver = db.query(Question_options_answers).filter(
            Question_options_answers.question_option_id == form.question_option_id,
            Question_options_answers.question_state_id == form.question_state_id,
            Question_options_answers.answer == form.answer).first()
    if qoa_ver and qoa.answer == form.answer:
        raise HTTPException(status_code=400, detail="Bu javob bu holat va variant uchun mavjud")
    db.query(Question_options_answers).filter(Question_options_answers.id == form.id).update({
        Question_options_answers.question_option_id: form.question_option_id,
        Question_options_answers.question_state_id: form.question_state_id,
        Question_options_answers.answer: form.answer,
        Question_options_answers.comment: form.comment,
        Question_options_answers.user_id: thisuser.id,
    })
    db.commit()