from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one, the_one_username
from utils.pagination import pagination
from models.question_types import Question_types


def all_question_types(search, page, limit, db):
    question_types = db.query(Question_types).options(joinedload(Question_types.user))
    if search:
        search_formatted = "%{}%".format(search)
        question_types = question_types.filter(
            Question_types.name.like(search_formatted) | Question_types.comment.like(search_formatted))
    else:
        question_types = question_types.filter(Question_types.id > 0)

    question_types = question_types.order_by(Question_types.id.desc())
    return pagination(question_types, page, limit)


def create_question_type(form, db, thisuser):
    new_question_type_db = Question_types(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id,
    )

    save_in_db(db=Question_types, obj=new_question_type_db)

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_question_type(db, id):
    the_item = db.query(Question_types).options(
        joinedload(Question_types.user)).filter(Question_types.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question_type mavjud emas")


def update_question_type(form, thisuser, db):
    the_one(db=db, model=Question_types, id=form.id)

    db.query(Question_types).filter(Question_types.id == form.id).update({
        Question_types.name: form.name,
        Question_types.comment: form.comment,
        Question_types.user_id: thisuser.id,

    })

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


