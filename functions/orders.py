from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.orders import Orders
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_orders(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Orders.name.like(search_formatted) | Orders.number.like(search_formatted) | Orders.username.like(
            search_formatted)
    else:
        search_filter = Orders.id > 0
    if status in [True, False]:
        status_filter = Orders.status == status
    else:
        status_filter = Orders.id > 0

    users = db.query(Orders).filter(search_filter, status_filter, ).order_by(Orders.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_order(id, db):
    return db.query(Orders).filter(Orders.id == id).first()


def order_current(user, db):
    return db.query(Orders).filter(Orders.id == user.id).first()


def create_order(form, user, db):
    user_verification = db.query(Orders).filter(Orders.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Orders).filter(Orders.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Orders(
        user_id=form.user_id,


    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_order(form, user, db):
    if one_order(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Orders).filter(Orders.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.id: form.id,
        Orders.user_id: form.user_id,
        Orders.date: form.date,
        Orders.status: form.status,



    })
    db.commit()

    return one_order(form.id, db)


def update_order_salary(id, salary, db):
    if one_order(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli buyurtma mavjud emas")

    db.query(Orders).filter(Orders.id == id).update({
        Orders.salary: salary,

    })
    db.commit()
    return one_order(id, db)


def order_delete(id, db):
    if one_order(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Orders).filter(Orders.id == id).update({
        Orders.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}


