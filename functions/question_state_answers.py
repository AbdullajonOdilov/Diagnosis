from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.question_state_options import Question_state_options
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.question_state_answers import Question_state_answers


def all_question_state_answers(search, question_state_option_id,  page, limit, db):
    question_state_answers = db.query(Question_state_answers).options(joinedload(Question_state_answers.user),
                                                                      joinedload(Question_state_answers.question_state_option))
    if search:
        search_formatted = "%{}%".format(search)
        question_state_answers = question_state_answers.filter(Question_state_answers.answer.like(search_formatted)
                                                               | Question_state_answers.comment.like(search_formatted))
    if question_state_option_id:
        question_state_answers = question_state_answers.\
            filter(Question_state_answers.question_state_option_id == question_state_option_id)

    question_state_answers = question_state_answers.order_by(Question_state_answers.id.desc())
    return pagination(question_state_answers, page, limit)


def one_question_state_answer(db, id):
    the_item = db.query(Question_state_answers).options(joinedload(Question_state_answers.user), joinedload(Question_state_answers.question_state_option, ),
                                              ).filter(
        Question_state_answers.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question_state mavjud emas")


def create_question_state_answer(form, thisuser, db):
    the_one(db, Question_state_options, form.question_state_option_id)
    if db.query(Question_state_answers).filter(Question_state_answers.question_state_option_id == form.question_state_option_id,
                                               Question_state_answers.answer == form.answer).first():
        raise HTTPException(status_code=400, detail="Bu javob bu holat option uchn mavjud")
    new_question_state_db = Question_state_answers(
        question_state_option_id=form.question_state_option_id,
        answer=form.answer,
        comment=form.comment,
        user_id=thisuser.id,
    )
    save_in_db(db, new_question_state_db)


def update_question_state_answer(form, thisuser, db):
    qsa = the_one(db=db, model=Question_state_answers, id=form.id)
    the_one(db, Question_state_options, form.question_state_option_id)
    qsa_ver = db.query(Question_state_answers).filter(
            Question_state_answers.question_state_option_id == form.question_state_option_id,
            Question_state_answers.answer == form.answer).first()
    if qsa_ver and qsa.answer == form.answer:
        raise HTTPException(status_code=400, detail="Bu javob bu holat option uchn mavjud")
    db.query(Question_state_answers).filter(Question_state_answers.id == form.id).update({
        Question_state_answers.question_state_option_id: form.question_state_option_id,
        Question_state_answers.answer: form.answer,
        Question_state_answers.comment: form.comment,
        Question_state_answers.user_id: thisuser.id,
    })
    db.commit()