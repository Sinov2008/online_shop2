import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.orders import all_orders, one_Order, update_Order, delete_Order, add_Order
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)
from schemas.orders import OrderUpdate,OrderCreate
from schemas.users import UserCurrent

order_router = APIRouter()


@order_router.post('/add', )
def add_order(form: OrderCreate, db: Session = Depends(get_db),
              current_user: UserCurrent = Depends(get_current_active_user)):  #
    if add_Order(form, current_user, db):
        raise HTTPException(status_code=200, detail="A`maliyot muvaffaqiyatli amalga oshirildi")


@order_router.get('/', status_code=200)
def get_order(search: str = None, status: bool = True, id: int = 0,
                start_date: date = datetime.datetime.now().date().min,
                end_date: date = datetime.datetime.now().date(),
                roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_Order(id,current_user, db)
    else:
        return all_orders(search, status, start_date, end_date, page, limit, db)


@order_router.put("/update")
def order_update(form: OrderUpdate, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    if update_Order(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@order_router.delete('/{id}', status_code=200)
def delete_order(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_Order(id,current_user,db)