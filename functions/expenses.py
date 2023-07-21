from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.expenses import Expenses
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_expenses(search, status,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Expenses.name.like(search_formatted) | Expenses.number.like(search_formatted) | Expenses.username.like(
            search_formatted)
    else:
        search_filter = Expenses.id > 0
    if status in [True, False]:
        status_filter = Expenses.status == status
    else:
        status_filter = Expenses.id > 0



    users = db.query(Expenses).filter(
        search_filter, status_filter,).order_by(Expenses.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_expenses(id, db):
    return db.query(Expenses).filter(Expenses.id == id).first()


def expenses_current(user, db):
    return db.query(Expenses).filter(Expenses.id == user.id).first()


def create_expenses(form, user, db):
    user_verification = db.query(Expenses).filter(Expenses.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Expenses).filter(Expenses.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Expenses(
        price=form.price,
        worker_id=form.worker_id,
        source=form.source,
        user_id=form.user_id,
        comment=form.comment,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_expenses(form, user, db):
    if one_expenses(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Expenses).filter(Expenses.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Expenses).filter(Expenses.id == form.id).update({
        Expenses.id: form.id,
        Expenses.price: form.price,
        Expenses.worker_id: form.worker_id,
        Expenses.source: form.source,
        Expenses.user_id: form.user_id,
        Expenses.comment: form.comment,
        Expenses.date: form.date,
        Expenses.status: form.status,

    })
    db.commit()

    return one_expenses(form.id, db)


def update_expenses_salary(id, salary, db):
    if one_expenses(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Expenses).filter(Expenses.id == id).update({
        Expenses.salary: salary,

    })
    db.commit()
    return one_expenses(id, db)


def expenses_delete(id, db):
    if one_expenses(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Expenses).filter(Expenses.id == id).update({
        Expenses.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
