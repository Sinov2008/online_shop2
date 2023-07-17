import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.customers import all_customers, one_customers, update_customers, delete_customers, add_customers
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)
from schemas.customers import CustmoerUpdate,CustomersCreate
from schemas.users import UserCurrent

customers_router = APIRouter()


@customers_router.post('/add', )
def addd_customers(form: CustomersCreate, db: Session = Depends(get_db),
              current_user: UserCurrent = Depends(get_current_active_user)):  #
    if add_customers(form, current_user, db):
        raise HTTPException(status_code=200, detail="A`maliyot muvaffaqiyatli amalga oshirildi")


@customers_router.get('/', status_code=200)
def get_customers(search: str = None, status: bool = True, id: int = 0,
                start_date: date = datetime.datetime.now().date().min,
                end_date: date = datetime.datetime.now().date(),
                roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_customers(id,current_user,db)
    else:
        return all_customers(search, status, start_date, end_date, page, limit, db)


@customers_router.put("/update")
def customers_update(form: CustmoerUpdate, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    if update_customers(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@customers_router.delete('/{id}', status_code=200)
def delete_customer(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_customers(id,current_user,db)