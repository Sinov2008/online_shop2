from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.incomes import Incomes
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_incomes(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Incomes.name.like(search_formatted) | Incomes.number.like(search_formatted) | Incomes.username.like(
            search_formatted)
    else:
        search_filter = Incomes.id > 0
    if status in [True, False]:
        status_filter = Incomes.status == status
    else:
        status_filter = Incomes.id > 0

    users = db.query(Incomes).filter(search_filter, status_filter, ).order_by(Incomes.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_incomes(id, db):
    return db.query(Incomes).filter(Incomes.id == id).first()


def incomes_current(user, db):
    return db.query(Incomes).filter(Incomes.id == user.id).first()


def create_incomes(form, user, db):
    user_verification = db.query(Incomes).filter(Incomes.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Incomes).filter(Incomes.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Incomes(
        price=form.price,
        order_id=form.order_id,
        user_id=form.user_id,
        comment=form.comment,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_incomes(form, user, db):
    if one_incomes(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Incomes).filter(Incomes.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Incomes).filter(Incomes.id == form.id).update({
        Incomes.id: form.id,
        Incomes.comment: form.comment,
        Incomes.price: form.price,
        Incomes.order_id: form.order_id,
        Incomes.date: form.date,
        Incomes.user_id: form.user_id,
        Incomes.status: form.status,



    })
    db.commit()

    return one_incomes(form.id, db)


def update_incomes_salary(id, salary, db):
    if one_incomes(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Incomes).filter(Incomes.id == id).update({
        Incomes.salary: salary,

    })
    db.commit()
    return one_incomes(id, db)


def incomes_delete(id, db):
    if one_incomes(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Incomes).filter(Incomes.id == id).update({
        Incomes.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
