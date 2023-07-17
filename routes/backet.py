import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.backet import all_backet, one_backet, update_backet, delete_backet, add_backet
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)
from schemas.backet import BacketUpdate,BacketCreate
from schemas.users import UserCurrent

backet_router = APIRouter()


@backet_router.post('/add', )
def addd_backet(form: BacketCreate, db: Session = Depends(get_db),
              current_user: UserCurrent = Depends(get_current_active_user)):  #
    if add_backet(form, current_user, db):
        raise HTTPException(status_code=200, detail="A`maliyot muvaffaqiyatli amalga oshirildi")


@backet_router.get('/', status_code=200)
def get_backet(search: str = None, status: bool = True, id: int = 0,
                start_date: date = datetime.datetime.now().date().min,
                end_date: date = datetime.datetime.now().date(),
                roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_backet(id,current_user, db)
    else:
        return all_backet(search, status, start_date, end_date, page, limit, db)


@backet_router.put("/update")
def backet_update(form: BacketUpdate, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    if update_backet(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@backet_router.delete('/{id}', status_code=200)
def delete_backe(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_backet(id,current_user,db)