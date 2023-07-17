import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.products import all_products, one_products, update_products, delete_products, add_products
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)
from schemas.products import ProductCreate, ProductUpdate
from functions.users import create_user
from schemas.users import UserCurrent

router_product = APIRouter()


@router_product.post('/add', )
def addding_product(form: ProductCreate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):  #
    if add_products(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_product.get('/', status_code=200)
def get_product(search: str = None, status: bool = True, id: int = 0,
                start_date: date = datetime.datetime.now().date().min,
                end_date: date = datetime.datetime.now().date(),
                roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_products(id, db)
    else:
        return all_products(search, status, start_date, end_date, page, limit, db)


@router_product.put("/update")
def product_update(form: ProductUpdate, db: Session = Depends(get_db),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    if update_products(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_product.delete('/{id}', status_code=200)
def delete_product(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_products(id,current_user,db)
