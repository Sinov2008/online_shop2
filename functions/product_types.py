from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.product_types import Product_types
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_product_types(search, status,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Product_types.name.like(search_formatted) | Product_types.id.like(
            search_formatted)
    else:
        search_filter = Product_types.id > 0
    if status in [True, False]:
        status_filter = Product_types.status == status
    else:
        status_filter = Product_types.id > 0

    users = db.query(Product_types).filter(search_filter, status_filter, ).order_by(Product_types.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_product_types(id, db):
    return db.query(Product_types).filter(Product_types.id == id).first()


def product_types_current(user, db):
    return db.query(Product_types).filter(Product_types.id == user.id).first()


def create_product_types(form, user, db):
    user_verification = db.query(Product_types).filter(Product_types.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Product_types).filter(Product_types.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Product_types(
        name=form.name,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_product_types(form, user, db):
    if one_product_types(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Product_types).filter(Product_types.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Product_types).filter(Product_types.id == form.id).update({
        Product_types.id: form.id,
        Product_types.name: form.name,
        Product_types.status: form.status,
        Product_types.date: form.date

    })
    db.commit()

    return one_product_types(form.id, db)


def update_product_types_salary(id, salary, db):
    if one_product_types(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Product_types).filter(Product_types.id == id).update({
        Product_types.salary: salary,

    })
    db.commit()
    return one_product_types(id, db)


def product_types_delete(id, db):
    if one_product_types(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Product_types).filter(Product_types.id == id).update({
        Product_types.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
