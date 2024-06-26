from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, source_id, page, limit, status, db):
    categories = db.query(Categories).options(joinedload(Categories.user),
                                              joinedload(Categories.category_files))
    if search:
        search_formatted = "%{}%".format(search)
        categories = categories.filter(Categories.name.like(search_formatted)
                                       | Categories.comment.like(search_formatted))
    if status in [True, False]:
        categories = categories.filter(Categories.status == status)

    if not source_id==None:
        categories = categories.filter(Categories.source_id == source_id)

    categories = categories.order_by(Categories.id.desc())
    return pagination(categories, page, limit)


def create_category(form, thisuser, db):
    if db.query(Categories).filter(Categories.name == form.name, Categories.source_id == form.source_id).first():
        raise HTTPException(status_code=400, detail="Bu nom bazada mavjud")
    new_category_db = Categories(
        name=form.name,
        comment=form.comment,
        source_id=form.source_id,
        user_id=thisuser.id,
        )

    save_in_db(db, new_category_db)


def one_category(db, id):
    the_item = db.query(Categories).options(
        joinedload(Categories.user)).filter(Categories.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday category mavjud emas")


def update_category(form, thisuser, db):
    category = the_one(db=db, model=Categories, id=form.id)
    category_ver = db.query(Categories).filter(Categories.name == form.name, Categories.source_id == form.source_id).first()
    if category_ver and category.name != form.name:
        raise HTTPException(status_code=400, detail="Bu nom bazada mavjud")
    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.comment: form.comment,
        Categories.source_id: form.source_id,
        Categories.status: form.status,
        Categories.user_id: thisuser.id,
    })
    db.commit()


def delete_category(id, db):
    the_one(db, Categories, id)
    db.query(Categories).filter(Categories.id == id).delete()
    db.commit()