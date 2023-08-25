from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.questions import Questions


def all_questions(search, category_id, question_type_id, page, limit, db):
    questions = db.query(Questions).options(joinedload(Questions.user), joinedload(Questions.category), joinedload(Questions.question_type))
    if search:
        search_formatted = "%{}%".format(search)
        questions = questions.filter(
            Questions.name.like(search_formatted) | Questions.comment.like(search_formatted)
            |Questions.step.like(search_formatted))
    else:
        questions = questions.filter(Questions.id > 0)
    
    if category_id:
        questions = questions.filter(Questions.category_id == category_id)

    else:
        questions = questions
    if category_id:
        questions = questions.filter(Questions.question_type_id == question_type_id)
    else:
        questions = questions

    questions = questions.order_by(Questions.id.desc())
    return pagination(questions, page, limit)


def create_question(form, db, thisuser):
    new_question_db = Questions(
        name=form.name,
        comment=form.comment,
        category_id=form.category_id,
        question_type_id=form.question_type_id,
        step=form.step,
        user_id=thisuser.id,
    )

    save_in_db(db=Questions, obj=new_question_db)

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_question(db, id):
    the_item = db.query(Questions).options(
        joinedload(Questions.user),joinedload(Questions.category), joinedload(Questions.question_type)).filter(Questions.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question mavjud emas")


def update_question(form, thisuser, db):
    the_one(db=db, model=Questions, id=form.id)

    db.query(Questions).filter(Questions.id == form.id).update({
        Questions.name: form.name,
        Questions.comment: form.comment,
        Questions.category_id: form.category_id,
        Questions.step: form.step,
        Questions.question_type_id: form.question_type_id,
        Questions.user_id: thisuser.id,

    })

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


