
from models.expenses import Expenses



from fastapi import *

import datetime

from utils.pagination import pagination




def all_expenses(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Expenses.sourke.like(search_formatted) | \
                        Expenses.comment.like(search_formatted) | \
                        Expenses.worker_id.like(search_formatted)|\
                        Expenses.status.like(search_formatted)|Expenses.user_id.like(search_formatted)

    else:
        search_filter = Expenses.id > 0
    if status in [True, False]:
        status_filter = Expenses.status == status
    else:
        status_filter = Expenses.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min  # 00-00-00
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    dones = db.query(Expenses).filter(Expenses.date > start_date).filter(
        Expenses.date <= end_date).filter(search_filter, status_filter).order_by(Expenses.id.desc()
                                                                                )
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all

def one_produc(id, db):
    return db.query(Expenses).filter(Expenses.id == id).first()

def add_expenses(form,user,db):
    new_expenses = Expenses(
        sourke=form.sourke,
        comment=form.comment,
        worker_id=form.worker_id,
        status=form.status,
        price=form.price,
        user_id=user.id
    )
    db.add(new_expenses)
    db.commit()
    db.refresh(new_expenses)
    return {"date": "Ma'lumot saqlandi"}


def read_expenses(db):
    exepenses = db.query(Expenses).all()
    return exepenses


def one_expenses(id: int,ex, db):
    exepenses = db.query(Expenses).filter(Expenses.id == id).first()
    return exepenses

def update_expenses(form,ex,db):
    if one_produc(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Expenses).filter(Expenses.id == form.id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    user = db.query(Expenses).filter(Expenses.id == form.id).update(
        {
            Expenses.id:form.id,
            Expenses.user_id: form.user_id,
            Expenses.status: form.status,
            Expenses.sourke: form.sourke,
            Expenses.comment: form.comment,
            Expenses.worker_id: form.worker_id,
            Expenses.price: form.price,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_expenses(id:int,ex,db ):
    order = db.query(Expenses).filter(Expenses.id == id).update(
        {
            Expenses.status:False
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'chirildi"}
