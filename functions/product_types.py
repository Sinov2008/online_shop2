from fastapi import *

import datetime

from sqlalchemy.orm import joinedload

from utils.pagination import pagination

from models.product_types import Product_types



def all_product_type(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Product_types.name.like(search_formatted)|\
                        Product_types.status.like(search_formatted)

    else:
        search_filter = Product_types.id > 0
    if status in [True, False]:
        status_filter = Product_types.status == status
    else:
        status_filter = Product_types.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min#00-00-00
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyyy-mmm-dd formatida yozing  ")
    # dones = db.query(Product_types).filter(Product_types.date > start_date).filter(
    #     Product_types.date <= end_date).filter(search_filter, status_filter).order_by(Product_types.id.desc()
    # )
    types = db.query(Product_types).options(joinedload(Product_types.savdolar)).filter(search_filter, status_filter,).order_by(Product_types.id.desc())
    if page and limit:
        return pagination(types,page,limit)
    else:
        return types.all

def one_produc(id, db):
    return db.query(Product_types).filter(Product_types.id == id).first()



def add_product_type(form,type, db):
    new_products_type = Product_types(
        name=form.name,
        status=form.status,
    )
    db.add(new_products_type)
    db.commit()
    db.refresh(new_products_type)
    return {"date": "Ma'lumot saqlandi"}


def read_product_type(db):
    products_typ = db.query(Product_types).all()
    return products_typ


def one_product_type(id: int,type, db):
    produc_typ = db.query(Product_types).filter(Product_types.id == id).first()
    return produc_typ

def update_product_type(form,type,db):
    if one_produc(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Product_types).filter(Product_types.name == form.name).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    user = db.query(Product_types).filter(Product_types.id == form.id).update(
        {
            Product_types.id:form.id,
            Product_types.name: form.name,
            Product_types.status: form.status,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_product_type(id:int,type,db ):
    Produc_types = db.query(Product_types).filter(Product_types.id == id).update(
        {
            Product_types.status:False
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'chirildi"}