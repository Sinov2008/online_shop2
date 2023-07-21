from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.products import Products
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_products(search, status,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Products.name.like(search_formatted) | Products.number.like(search_formatted) | Products.username.like(
            search_formatted) | Products.roll.like(search_formatted)
    else:
        search_filter = Products.id > 0
    if status in [True, False]:
        status_filter = Products.status == status
    else:
        status_filter = Products.id > 0



    users = db.query(Products).filter(
        search_filter, status_filter,).order_by(Products.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_product(id, db):
    return db.query(Products).filter(Products.id == id).first()


def products_current(user, db):
    return db.query(Products).filter(Products.id == user.id).first()


def create_product(form, user, db):
    user_verification = db.query(Products).filter(Products.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday products mavjud")
    number_verification = db.query(Products).filter(Products.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Products(
        name=form.name,
        old_price=form.old_price,
        new_price=form.new_price,
        birlik=form.birlik,
        type=form.type,
        user_id=user.id



    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_products(form, user, db):
    if one_product(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Products).filter(Products.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Products).filter(Products.id == form.id).update({
        Products.id: form.id,
        Products.name: form.name,
        Products.status: form.status,
        Products.old_price: form.old_price,
        Products.new_price: form.new_price,

    })
    db.commit()

    return one_product(form.id, db)


def update_products_salary(id, salary, db):
    if one_product(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Products).filter(Products.id == id).update({
        Products.salary: salary,

    })
    db.commit()
    return one_product(id, db)


def products_delete(id, db):
    if one_product(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Products).filter(Products.id == id).update({
        Products.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
