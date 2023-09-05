from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.customers import Customers
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.diagnostics import Diagnostics


def all_diagnostics(customer_id, category_id, status, page, limit, db):
    diagnostics = db.query(Diagnostics).options(joinedload(Diagnostics.user),
                                                joinedload(Diagnostics.customer),
                                                joinedload(Diagnostics.category))

    if customer_id:
        diagnostics = diagnostics.filter(Diagnostics.customer_id == customer_id)
    if category_id:
        diagnostics = diagnostics.filter(Diagnostics.category_id == category_id)
    if status in [True, False]:
        diagnostics = diagnostics.filter(Diagnostics.status == status)

    diagnostics = diagnostics.order_by(Diagnostics.id.desc())
    return pagination(diagnostics, page, limit)


def create_diagnostics(form, thisuser, db):
    the_one(db, Customers, form.customer_id)
    the_one(db, Categories, form.category_id)
    new_diagnostics_db = Diagnostics(
        customer_id=form.customer_id,
        category_id=form.category_id,         
        user_id=thisuser.id,
    )
    save_in_db(db, new_diagnostics_db)


def one_diagnostics(db, id):
    the_item = db.query(Diagnostics).options(joinedload(Diagnostics.user),
                                             joinedload(Diagnostics.customer),
                                             joinedload(Diagnostics.category)).filter(
        Diagnostics.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday diagnostics mavjud emas")


def update_diagnostics(form, thisuser, db):
    the_one(db=db, model=Diagnostics, id=form.id)
    the_one(db, Customers, form.customer_id)
    the_one(db, Categories, form.category_id)
    db.query(Diagnostics).filter(Diagnostics.id == form.id).update({
        Diagnostics.customer_id: form.customer_id,
        Diagnostics.category_id: form.category_id,         
        Diagnostics.user_id: thisuser.id,
    })
    db.commit()
