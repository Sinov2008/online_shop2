from models.products import Products
from schemas.products import *
import datetime
from utils.pagination import pagination
from fastapi import *

def all_products(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Products.name.like(search_formatted)|\
                        Products.birlik.like(search_formatted)|Products.type.like(search_formatted)

    else:
        search_filter = Products.id > 0
    if status in [True, False]:
        status_filter = Products.status == status
    else:
        status_filter = Products.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min#00-00-00
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyyy-mmm-dd formatida yozing  ")
    dones = db.query(Products).filter(Products.date > start_date).filter(
        Products.date <= end_date).filter(search_filter, status_filter).order_by(Products.id.desc()
    )
    if page and limit:
        return pagination(dones,page,limit)
    else:
        return dones.all

def one_produc(id, db):
    return db.query(Products).filter(Products.id == id).first()




def add_products(form,pr,db):
    new_products = Products(
        name=form.name,
        type=form.type,
        old_price=form.old_price,
        new_price=form.new_price,
        birlik=form.birlik,
        user_id=pr.id

    )
    db.add(new_products)
    db.commit()
    db.refresh(new_products)
    return {"date": "Ma'lumot saqlandi"}


def read_products(db):
    products = db.query(Products).all()
    return products


def one_products(id: int, db):
    produc = db.query(Products).filter(Products.id == id).first()
    return produc




def update_products(form,product,db):
    if one_produc(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Products).filter(Products.name == form.name).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    user = db.query(Products).filter(Products.id == form.id).update(
        {
            Products.id:form.id,
            Products.name: form.name,
            Products.birlik: form.birlik,
            Products.type: form.type,
            Products.status: form.status,
            Products.old_price:form.old_price,
            Products.new_price: form.new_price,
            Products.user_id: form.user_id,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_products(id:int,product,db ):
    user = db.query(Products).filter(Products.id == id).update(
        {
            Products.status: False,
        }
    )

    db.commit()
    return {"date": "Ma'lumot o'chirildi"}
