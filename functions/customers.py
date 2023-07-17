from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from fastapi import *
from db import Base, get_db
import datetime
from models.customers import Customers
from utils.pagination import pagination

from schemas.users import *

def all_customers(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Customers.name.like(search_formatted)|\
                        Customers.phone.like(search_formatted)|Customers.address.like(search_formatted)

    else:
        search_filter = Customers.id > 0
    if status in [True, False]:
        status_filter = Customers.status == status
    else:
        status_filter = Customers.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min#00-00-00
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyyy-mmm-dd formatida yozing  ")
    # dones = db.query(Customers).filter(Customers.date > start_date).filter(
    #     Customers.date <= end_date).filter(search_filter, status_filter).order_by(Customers.id.desc()
    # )
    customer = db.query(Customers).options(joinedload(Customers.savdo),joinedload(Customers.savdolari)).filter(search_filter, status_filter).order_by(Customers.id.desc())
    if page and limit:
        return pagination(customer,page,limit)
    else:
        return customer.all

def one_produc(id, db):
    return db.query(Customers).filter(Customers.id == id).first()


def add_customers(form,df,db):
    new_expenses = Customers(
        name=form.name,
        phone=form.phone,
        address=form.address,
    )
    db.add(new_expenses)
    db.commit()
    db.refresh(new_expenses)
    return {"data": "Ma'lumot saqlandi"}


def read_customers(db):
    exepenses = db.query(Customers).all()
    return exepenses


def one_customers(id: int,cu, db):
    exepenses = db.query(Customers).filter(Customers.id == id).first()
    return exepenses

def update_customers(form,cu,db):
    if one_produc(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Customers).filter(Customers.name == form.name).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    user = db.query(Customers).filter(Customers.id == form.id).update(
        {
            Customers.id:form.id,
            Customers.name:form.name,
            Customers.status: form.status,
            Customers.phone: form.phone,
            Customers.address: form.address,
        }
    )
    db.commit()
    return {"data":"Ma'lumot o'zgartirildi"}

def delete_customers(id:int,cu,db ):
    order = db.query(Customers).filter(Customers.id == id).update(
        {
            Customers.status:False
        }
    )
    db.commit()
    return {"data": "Ma'lumot o'chirildi"}
