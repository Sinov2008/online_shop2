import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.product_types import all_product_type, one_product_type, update_product_type, delete_product_type, add_product_type
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)
from schemas.product_types import Product_typeUpdate, Product_typeCreate
from schemas.users import UserCurrent

product_type_router = APIRouter()


@product_type_router.post('/add', )
def add_product_ty(form: Product_typeCreate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):  #
    if add_product_type(form, current_user, db):
        raise HTTPException(status_code=200, detail="A`maliyot muvaffaqiyatli amalga oshirildi")


@product_type_router.get('/', status_code=200)
def get_product_ty(search: str = None, status: bool = True, id: int = 0,
                start_date: date = datetime.datetime.now().date().min,
                end_date: date = datetime.datetime.now().date(),
                roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_product_type(id,current_user, db)
    else:
        return all_product_type(search, status, start_date, end_date, page, limit, db)


@product_type_router.put("/update")
def product_update_ty(form: Product_typeUpdate, db: Session = Depends(get_db),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    if update_product_type(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@product_type_router.delete('/{id}', status_code=200)
def delete_product_ty(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_product_type(id,current_user,db)
