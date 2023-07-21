from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.backet import Backet
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_backet(search, status,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Backet.name.like(search_formatted) | Backet.quantity.like(search_formatted) | Backet.status.like(
            search_formatted)
    else:
        search_filter = Backet.id > 0
    if status in [True, False]:
        status_filter = Backet.status == status
    else:
        status_filter = Backet.id > 0


    users = db.query(Backet).filter(search_filter, status_filter, ).order_by(Backet.name.asc())
    if page and limit:
        return pagination(users, page,  limit)
    else:
        return users.all()


def one_backet(id, db):
    return db.query(Backet).filter(Backet.id == id).first()


def backet_current(user, db):
    return db.query(Backet).filter(Backet.id == user.id).first()


def create_backet(form, user, db):
    user_verification = db.query(Backet).filter(Backet.name == form.name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Backet).filter(Backet.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Backet(
        name=form.name,
        quantity=form.quantity,
        order_id=form.order_id,
        user_id=form.user_id,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_backet(form, user, db):
    if one_backet(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Backet).filter(Backet.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Backet).filter(Backet.id == form.id).update({
        Backet.id: form.id,
        Backet.name: form.name,
        Backet.quantity: form.quantity,
        Backet.order_id: form.order_id,
        Backet.date: form.date,
        Backet.user_id: form.user_id,
        Backet.status: form.status,

    })
    db.commit()

    return one_backet(form.id, db)


def update_backet_salary(id, salary, db):
    if one_backet(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Backet).filter(Backet.id == id).update({
        Backet.salary: salary,

    })
    db.commit()
    return one_backet(id, db)


def backet_delete(id, db):
    if one_backet(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Backet).filter(Backet.id == id).update({
        Backet.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
