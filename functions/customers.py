from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.customers import  Customers
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_customers(search, status,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Customers.name.like(search_formatted) | Customers.number.like(search_formatted) | Customers.username.like(
            search_formatted)
    else:
        search_filter = Customers.id > 0
    if status in [True, False]:
        status_filter = Customers.status == status
    else:
        status_filter = Customers.id > 0



    users = db.query(Customers).filter(
        search_filter, status_filter, ).order_by(Customers.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_customers(id, db):
    return db.query(Customers).filter(Customers.id == id).first()


def customers_current(user, db):
    return db.query(Customers).filter(Customers.id == user.id).first()


def create_customers(form, user, db):
    user_verification = db.query(Customers).filter(Customers.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Customers).filter(Customers.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Customers(
        name=form.name,
        phone=form.phone,
        address=form.address,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_customers(form, user, db):
    if one_customers(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Customers).filter(Customers.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.id: form.id,
        Customers.name: form.name,
        Customers.phone: form.phone,
        Customers.address: form.address,
        Customers.date: form.date,
        Customers.status: form.status,

    })
    db.commit()

    return one_customers(form.id, db)


def update_user_salary(id, salary, db):
    if one_customers(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Customers).filter(Customers.id == id).update({
        Customers.salary: salary,

    })
    db.commit()
    return one_customers(id, db)


def user_delete(id, db):
    if one_customers(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Customers).filter(Customers.id == id).update({
        Customers.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
