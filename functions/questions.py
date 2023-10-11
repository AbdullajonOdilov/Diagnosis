from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.question_types import Question_types
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.questions import Questions


def all_questions(search, category_id, question_type_id, page, limit, db):
    questions = db.query(Questions).options(joinedload(Questions.question),
        joinedload(Questions.user), joinedload(Questions.diagnosis_option_question),
        joinedload(Questions.category).load_only(Categories.name),
        joinedload(Questions.question_type))

    if search:
        search_formatted = "%{}%".format(search)
        questions = questions.filter(
            Questions.name.like(search_formatted) | Questions.comment.like(search_formatted))
    if category_id:
        questions = questions.filter(Questions.category_id == category_id)
    if question_type_id:
        questions = questions.filter(Questions.question_type_id == question_type_id)

    questions = questions.order_by(Questions.id.desc())
    return pagination(questions, page, limit)


def create_question(form, thisuser, db):
    the_one(db, Categories, form.category_id)
    the_one(db, Question_types, form.question_type_id)
    existing_question = db.query(Questions).filter(Questions.name == form.name,
                                                   Questions.category_id == form.category_id).first()

    if existing_question:
        raise HTTPException(status_code=400, detail="Bu kategoriya uchun bu savol mavjud!")

    new_question_db = Questions(
        name=form.name,
        comment=form.comment,
        category_id=form.category_id,
        question_type_id=form.question_type_id,
        step=form.step,
        user_id=thisuser.id,
    )
    save_in_db(db, new_question_db)
    return new_question_db.id


def one_question(db, id):
    the_item = db.query(Questions).join(Questions.question).options(joinedload(Questions.question),
        joinedload(Questions.user), joinedload(Questions.diagnosis_option_question),
        joinedload(Questions.category).load_only(Categories.name),
        joinedload(Questions.question_type)).filter(Questions.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question mavjud emas")


def update_question(form, thisuser, db):
    question = the_one(db=db, model=Questions, id=form.id)
    the_one(db, Categories, form.category_id)
    the_one(db, Question_types, form.question_type_id)
    question_ver = db.query(Questions).filter(Questions.name == form.name, Questions.category_id == form.category_id).first()
    if question_ver and question.name != form.name:
        raise HTTPException(status_code=400, detail=f"Bu nom bazada mavjud")

    db.query(Questions).filter(Questions.id == form.id).update({
        Questions.name: form.name,
        Questions.comment: form.comment,
        Questions.category_id: form.category_id,
        Questions.step: form.step,
        Questions.question_type_id: form.question_type_id,
        Questions.user_id: thisuser.id,
    })
    db.commit()
