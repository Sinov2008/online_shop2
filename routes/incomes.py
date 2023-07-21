from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user
Base.metadata.create_all(bind=engine)
from functions.incomes import one_incomes, all_incomes, update_incomes, create_incomes, incomes_delete,incomes_current
from schemas.users import UserBase,UserCreate,UserUpdate,UserCurrent

router_incomes = APIRouter()



@router_incomes.post('/add', )
def add_incomes(form: UserCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_incomes(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_incomes.get('/',  status_code = 200)
def get_incomes(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_incomes(id, db)
    else :
        return all_incomes(search, status,roll, page, limit, db)

@router_incomes.get('/user',  status_code = 200)
def get_incomes_current(db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return incomes_current(current_user, db)


@router_incomes.put("/update")
def incomes_update(form: UserUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_incomes(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_incomes.delete('/{id}',  status_code = 200)
def delete_incomes(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return incomes_delete(id, db)