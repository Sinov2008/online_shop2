
from models.backet import Backet



from fastapi import *

import datetime

from utils.pagination import pagination


def all_backet(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Backet.name.like(search_formatted) | \
                        Backet.user_id.like(search_formatted) | \
                        Backet.status.like(search_formatted)

    else:
        search_filter = Backet.id > 0
    if status in [True, False]:
        status_filter = Backet.status == status
    else:
        status_filter = Backet.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min  # 00-00-00
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    dones = db.query(Backet).filter(Backet.date > start_date).filter(
        Backet.date <= end_date).filter(search_filter, status_filter).order_by(Backet.id.desc()
                                                                                 )
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all


def one_produc(id, db):
    return db.query(Backet).filter(Backet.id == id).first()


def add_backet(form,sd,db):
    new_expenses = Backet(
        name=form.name,
        status=form.status,
        order_id=form.order_id,
        customer_id=form.customer_id,
        quantity=form.quantity,
    )
    db.add(new_expenses)
    db.commit()
    db.refresh(new_expenses)
    return {"date": "Ma'lumot saqlandi"}


def read_backet(db):
    exepenses = db.query(Backet).all()
    return exepenses


def one_backet(id: int,ba, db):
    exepenses = db.query(Backet).filter(Backet.id == id).first()
    return exepenses

def update_backet(form,ba,db):
    if one_produc(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Backet).filter(Backet.name == form.name).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    user = db.query(Backet).filter(Backet.id == form.id).update(
        {
            Backet.id:form.id,
            Backet.name:form.name,
            Backet.status: form.status,
            Backet.order_id: form.order_id,
            Backet.quantity: form.quantity,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_backet(id:int,ba,db ):
    order = db.query(Backet).filter(Backet.id == id).update(
        {
            Backet.status:False
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'chirildi"}
