import os
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.categories import Categories
from models.customers import Customers
from models.question_states import Question_states
from models.uploaded_files import Uploaded_files
from models.users import Users
from utils.db_operations import the_one
from utils.pagination import pagination


def all_uploaded_files(search, source, page, limit, db):
    uploaded = db.query(Uploaded_files).options(joinedload(Uploaded_files.user),
                                                joinedload(Uploaded_files.category_source).load_only(Categories.name))
    if source:
        uploaded = uploaded.filter(Uploaded_files.source == source)
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = uploaded.filter(Uploaded_files.comment.like(search_formatted))
    else:
        search_filter = Uploaded_files.id > 0
    uploaded = uploaded.filter(search_filter).order_by(Uploaded_files.id.desc())
    return pagination(uploaded, page, limit)


def one_file(ident, db):
    the_item = db.query(Uploaded_files).filter(Uploaded_files.id == ident).options(
        joinedload(Uploaded_files.user), joinedload(Uploaded_files.category).load_only(Categories.name)).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail=f"Bazada bunday ma'lumot mavjud emas")
    return the_item


def create_file(new_files, source, source_id, comment, thisuser, db):
    if (source == "category" and db.query(Categories).filter(Categories.id == source_id).first() is None) or \
            (source == "user" and db.query(Users).filter(Users.id == source_id).first() is None) or \
            (source == "customer" and db.query(Customers).filter(Customers.id == source_id).first() is None) or \
            (source == "question_state" and db.query(Question_states).filter(Question_states.id == source_id).first() is None):
        raise HTTPException(status_code=400, detail="source va source_id bir-biriga mos kelmadi!")
    uploaded_file_objects = []

    for new_file in new_files:
        ext = os.path.splitext(new_file.filename)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg",'.pdf']:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        file_location = f"uploaded_files/{new_file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(new_file.file.read())

        new_file_db = Uploaded_files(
            file=file_location,
            source=source,
            source_id=source_id,
            comment=comment,
            user_id=thisuser.id,
        )
        uploaded_file_objects.append(new_file_db)

    db.add_all(uploaded_file_objects)
    db.commit()


def delete_file(id, db):
    the_one(db, Uploaded_files, id)
    db.query(Uploaded_files).filter(Uploaded_files.id == id).delete()
    db.commit()


def update_file(new_files, source, source_id, comment, this_user, db):
    items = db.query(Uploaded_files).filter(Uploaded_files.source == source,
                                            Uploaded_files.source_id == source_id).all()
    for item in items:
        delete_file(item.id, db)
    create_file(new_files, source, source_id, comment, this_user, db)



