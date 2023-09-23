from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.question_types import Question_types
from utils.db_operations import the_one, save_in_db, the_one_model_name
from utils.pagination import pagination


def all_question_types(search, page, limit, db):
    question_types = db.query(Question_types).options(joinedload(Question_types.user))
    if search:
        search_formatted = "%{}%".format(search)
        question_types = question_types.filter(Question_types.name.ilike(search_formatted)
                                               | Question_types.comment.ilike(search_formatted))

    question_types = question_types.order_by(Question_types.id.desc())
    return pagination(question_types, page, limit)


def create_question_type(form, thisuser,  db):
    the_one_model_name(db, Question_types, form.name)
    new_q_type_db = Question_types(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id
    )
    save_in_db(db, new_q_type_db)


def one_question_type(db, ident):
    the_item = db.query(Question_types).options(
        joinedload(Question_types.user)).filter(Question_types.id == ident).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday ma'lumot mavjud emas")


def update_question_type(form, thisuser, db):
    question_type = the_one(db=db, model=Question_types, id=form.id)
    question_type_ver = db.query(Question_types).filter(Question_types.name == form.name).first()
    if question_type_ver and question_type_ver.id != question_type.id:
        raise HTTPException(status_code=400, detail=f"Bu nom bazada mavjud")
    db.query(Question_types).filter(Question_types.id == form.id).update({
        Question_types.name: form.name,
        Question_types.comment: form.comment,
        Question_types.user_id: thisuser.id
    })
    db.commit()


def delete_question_type(id, db):
    the_one(db, Question_types, id)
    db.query(Question_types).filter(Question_types.id == id).delete()
    db.commit()
