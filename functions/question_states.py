from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.question_states import Question_states


def all_question_states(search, page, limit,  db):
    question_states = db.query(Question_states).\
        options(joinedload(Question_states.user), joinedload(Question_states.state_files))

    if search:
        search_formatted = "%{}%".format(search)
        question_states = question_states.filter(
            Question_states.name.like(search_formatted) | Question_states.comment.like(search_formatted))
   
    question_states = question_states.order_by(Question_states.id.desc())
    return pagination(question_states, page, limit)


def create_question_state(form, thisuser,  db):
    the_one_model_name(db, Question_states, form.name)
    new_question_state_db = Question_states(
        name=form.name,
        comment=form.comment,       
        user_id=thisuser.id,
    )

    save_in_db(db, new_question_state_db)


def one_question_state(db, id):
    the_item = db.query(Question_states).\
        options(joinedload(Question_states.user), joinedload(Question_states.state_files)).filter(Question_states.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday question_state mavjud emas")


def update_question_state(form, thisuser, db):
    state = the_one(db=db, model=Question_states, id=form.id)
    state_ver = db.query(Question_states).filter(Question_states.name == form.name).first()
    if state_ver and state.name != form.name:
        raise HTTPException(status_code=400, detail=f"Bu nom bazada mavjud")

    db.query(Question_states).filter(Question_states.id == form.id).update({
        Question_states.name: form.name,
        Question_states.comment: form.comment,
        Question_states.user_id: thisuser.id,
    })
    db.commit()
