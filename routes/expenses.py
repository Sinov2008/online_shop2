from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user
Base.metadata.create_all(bind=engine)
from functions.expenses import one_expenses, all_expenses, update_expenses, create_expenses, expenses_delete, expenses_current
from schemas.expenses import ExpensesBase,ExpensesCreate,ExpensesUpdate,ExpensesCurrent

router_expenses = APIRouter()



@router_expenses.post('/add', )
def add_expenses(form: ExpensesCreate, db: Session = Depends(get_db),current_user: ExpensesCurrent = Depends(get_current_active_user) ) : #
    if create_expenses(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_expenses.get('/',  status_code = 200)
def get_expenses(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: expenses_current = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_expenses(id, db)
    else :
        return all_expenses(search, status, page, limit, db)

@router_expenses.get('/user',  status_code = 200)
def get_expenses_current(db: Session = Depends(get_db),current_user: ExpensesCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return expenses_current(current_user, db)


@router_expenses.put("/update")
def expenses_update(form: ExpensesUpdate, db: Session = Depends(get_db),current_user: ExpensesCurrent = Depends(get_current_active_user)) :
    if update_expenses(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_expenses.delete('/{id}',  status_code = 200)
def delete_expenses(id: int = 0,db: Session = Depends(get_db), current_user: ExpensesCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return expenses_delete(id, db)