



from fastapi import *

import datetime
from models.orders import Orders
from utils.pagination import pagination

from schemas.users import *

def all_orders(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Orders.user_id.like(search_formatted)|\
                        Orders.status.like(search_formatted)

    else:
        search_filter = Orders.id > 0
    if status in [True, False]:
        status_filter = Orders.status == status
    else:
        status_filter = Orders.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min#00-00-00
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyyy-mmm-dd formatida yozing  ")
    dones = db.query(Orders).filter(Orders.date > start_date).filter(
        Orders.date <= end_date).filter(search_filter, status_filter).order_by(Orders.id.desc()
    )
    if page and limit:
        return pagination(dones,page,limit)
    else:
        return dones.all

def one_produc(id, db):
    return db.query(Orders).filter(Orders.id == id).first()


def add_Order(form,user,db):
    new_orders = Orders(
        status=form.status,
        customer_id=form.customer_id,
        user_id=user.id
    )
    db.add(new_orders)
    db.commit()
    db.refresh(new_orders)
    return {"date": "Ma'lumot saqlandi"}


def read_Order(db):
    orders = db.query(Orders).all()
    return orders


def one_Order(id: int,order, db):
    order = db.query(Orders).filter(Orders.id == id).first()
    return order

def update_Order(form,order,db):
    if one_produc(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Orders).filter(Orders.id == form.id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    user = db.query(Orders).filter(Orders.id == form.id).update(
        {
            Orders.id:form.id,
            Orders.user_id:form.user_id,
            Orders.status: form.status,
            Orders.customer_id: form.customer_id
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_Order(id:int,order,db ):
    order = db.query(Orders).filter(Orders.id == id).update(
        {
            Orders.status:False
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'chirildi"}

