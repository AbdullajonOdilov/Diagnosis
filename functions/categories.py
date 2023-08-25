from fastapi import HTTPException
from sqlalchemy.orm import joinedload

 
 
from routes.login import get_password_hash
from utils.db_operations import save_in_db, the_one, the_one_username
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, page, limit, status, db):
    categories = db.query(Categories).options(joinedload(Categories.user))
    if search:
        search_formatted = "%{}%".format(search)
        categories = categories.filter(Categories.name.like(search_formatted) | Categories.comment.like(search_formatted))
    else:
        categories = categories.filter(Categories.id > 0)
    if status:
        categories = categories.filter(Categories.status == True)
    elif status is False:
        categories = categories.filter(Categories.status == False)
    else:
        categories = categories
    categories = categories.order_by(Categories.id.desc())
    return pagination(categories, page, limit)


def create_category(form, db, thisuser):

    new_category_db = Categories(
        name=form.name,
        comment=form.comment,
        source_id=form.source_id,
        user_id=thisuser.id,
        )

    save_in_db(db=Categories,obj=new_category_db)
    
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_category(db, id):
    the_item = db.query(Categories).options(
        joinedload(Categories.user)).filter(Categories.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday category mavjud emas")


def update_category(form, thisuser, db):
    the_one(db=db, model=Categories, id=form.id)

    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.comment: form.comment,
        Categories.source_id: form.source_id,
        Categories.status: form.status,
        Categories.user_id: thisuser.id,

    })

   
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


