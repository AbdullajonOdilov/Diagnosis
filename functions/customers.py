from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, delete_phone
from models.customers import Customers
from models.phones import Phones
from utils.db_operations import the_one
from utils.pagination import pagination


def all_customers(status, search, page, limit, db):
    customers = db.query(Customers).options(joinedload(Customers.customer_phones),
                                            joinedload(Customers.customer_files),
                                            joinedload(Customers.user))
    if search:
        search_formatted = "%{}%".format(search)
        customers = customers.filter(Customers.name.ilike(search_formatted) | Customers.comment.ilike(search_formatted))

    if status in [True, False]:
        customers = customers.filter(Customers.status == status)
    customers = customers.order_by(Customers.id.desc())
    return pagination(customers, page, limit)


def create_customer(form, thisuser,  db):
    new_customer_db = Customers(
        name=form.name,
        address=form.address,
        comment=form.comment,
        user_id=thisuser.id
    )
    db.add(new_customer_db)
    db.flush()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='customer', source_id=new_customer_db.id, comment=comment, user_id=thisuser.id,
                     db=db, commit=False)
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_customer(db, ident):
    the_item = db.query(Customers).options(joinedload(Customers.customer_phones),
                                            joinedload(Customers.customer_files),
                                            joinedload(Customers.user)).filter(Customers.id == ident).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday customer mavjud emas")


def update_customer(form, thisuser, db):
    customer = the_one(db=db, model=Customers, id=form.id)
    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.name: form.name,
        Customers.address: form.address,
        Customers.comment: form.comment,
        Customers.user_id: thisuser.id
    })

    customer_phones = db.query(Phones).filter(Phones.source_id == customer.id).all()
    for phone in customer_phones:
        delete_phone(id=phone.id, db=db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='customer', source_id=customer.id, comment=comment, user_id=thisuser.id,
                     db=db, commit=False)
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def delete_customer(id, db):
    the_one(id, Customers, db)
    db.query(Customers).filter(Customers.id == id).delete()
    db.commit()
