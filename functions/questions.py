from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.question_types import Question_types
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.questions import Questions


def all_questions(search, category_id, question_type_id, page, limit, db):
    questions = db.query(Questions).options(joinedload(Questions.user),
                                            joinedload(Questions.category).load_only(Categories.name),
                                            joinedload(Questions.question_type))
    if search:
        search_formatted = "%{}%".format(search)
        questions = questions.filter(
            Questions.name.like(search_formatted) | Questions.comment.like(search_formatted))
    
    if category_id:
        questions = questions.filter(Questions.category_id == category_id)

    if category_id:
        questions = questions.filter(Questions.question_type_id == question_type_id)

    questions = questions.order_by(Questions.id.desc())
    return pagination(questions, page, limit)


def create_question(form, thisuser, db):
    the_one(db, Categories, form.category_id)
    the_one(db, Question_types, form.question_type_id)
    new_question_db = Questions(
        name=form.name,
        comment=form.comment,
        category_id=form.category_id,
        question_type_id=form.question_type_id,
        step=form.step,
        user_id=thisuser.id,
    )
    save_in_db(db, new_question_db)


def one_question(db, id):
    the_item = db.query(Questions).options(
        joinedload(Questions.user),joinedload(Questions.category), joinedload(Questions.question_type)).filter(Questions.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question mavjud emas")


def update_question(form, thisuser, db):
    the_one(db=db, model=Questions, id=form.id)
    the_one(db, Categories, form.category_id)
    the_one(db, Question_types, form.question_type_id)
    db.query(Questions).filter(Questions.id == form.id).update({
        Questions.name: form.name,
        Questions.comment: form.comment,
        Questions.category_id: form.category_id,
        Questions.step: form.step,
        Questions.question_type_id: form.question_type_id,
        Questions.user_id: thisuser.id,
    })
    db.commit()
