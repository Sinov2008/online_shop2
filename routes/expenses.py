import datetime
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.expenses import all_expenses, one_expenses, update_expenses, delete_expenses, add_expenses
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)
from schemas.expenses import ExpensesUpdate,ExpensesCreate
from schemas.users import UserCurrent

expenses_router = APIRouter()


@expenses_router.post('/add', )
def addd_expenses(form: ExpensesCreate, db: Session = Depends(get_db),
              current_user: UserCurrent = Depends(get_current_active_user)):  #
    if add_expenses(form, current_user, db):
        raise HTTPException(status_code=200, detail="A`maliyot muvaffaqiyatli amalga oshirildi")


@expenses_router.get('/', status_code=200)
def get_expenses(search: str = None, status: bool = True, id: int = 0,
                start_date: date = datetime.datetime.now().date().min,
                end_date: date = datetime.datetime.now().date(),
                roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_expenses(id,current_user, db)
    else:
        return all_expenses(search, status, start_date, end_date, page, limit, db)


@expenses_router.put("/update")
def expenses_update(form: ExpensesUpdate, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    if update_expenses(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@expenses_router.delete('/{id}', status_code=200)
def delete_expense(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_expenses(id,current_user,db)