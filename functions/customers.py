from fastapi import HTTPException
from sqlalchemy.orm import joinedload

 
from utils.db_operations import save_in_db, the_one, the_one_username
from utils.pagination import pagination
from models.customers import Customers


def all_customers(search, page, limit, status, db):
    customers = db.query(Customers).options(joinedload(Customers.user))
    if search:
        search_formatted = "%{}%".format(search)
        customers = customers.filter(
            Customers.name.like(search_formatted) | Customers.comment.like(search_formatted))
    else:
        customers = customers.filter(Customers.id > 0)
    if status:
        customers = customers.filter(Customers.status == True)
    elif status is False:
        customers = customers.filter(Customers.status == False)
    else:
        customers = customers
    customers = customers.order_by(Customers.id.desc())
    return pagination(customers, page, limit)


def create_customer(form, db, thisuser):

    new_customer_db = Customers(
        name=form.name,
        comment=form.comment,
        address=form.address,         
        user_id=thisuser.id,
    )

    save_in_db(db=Customers, obj=new_customer_db)

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_customer(db, id):
    the_item = db.query(Customers).options(
        joinedload(Customers.user)).filter(Customers.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Bunday customer mavjud emas")


def update_customer(form, thisuser, db):
    the_one(db=db, model=Customers, id=form.id)

    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.name: form.name,
        Customers.comment: form.comment,
        Customers.address: form.address,
        Customers.status: form.status,
        Customers.user_id: thisuser.id,

    })

    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


