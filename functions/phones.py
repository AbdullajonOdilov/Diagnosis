from fastapi import HTTPException
from models.phones import Phones


def create_phone(number, source, source_id, comment, user_id, db, commit=True):
    if db.query(Phones).filter(Phones.number == number, Phones.source == source).first():
        raise HTTPException(status_code=400, detail="Bu nomer bazada mavjud")
    new_phone_db = Phones(
        number=number,
        comment=comment,
        source=source,
        source_id=source_id,
        user_id=user_id
    )
    db.add(new_phone_db)

    if commit:
        db.commit()


def delete_phone(id, db):
    db.query(Phones).filter(Phones.id == id).delete()
    db.commit()

