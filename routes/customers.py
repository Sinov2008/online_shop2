from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user
Base.metadata.create_all(bind=engine)
from functions.customers import one_customers, all_customers, update_customers, create_customers, user_delete,customers_current
from schemas.customers import CustomersBase,CustomersCreate,CustomersUpdate,CustomersCurrent

router_customers = APIRouter()



@router_customers.post('/add', )
def add_user(form: CustomersCreate, db: Session = Depends(get_db),current_user: CustomersCurrent = Depends(get_current_active_user) ) : #
    if create_customers(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_customers.get('/',  status_code = 200)
def get_users(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: CustomersCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_customers(id, db)
    else :
        return all_customers(search, status, page, limit, db)

@router_customers.get('/user',  status_code = 200)
def get_user_current(db: Session = Depends(get_db),current_user: CustomersCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return customers_current(current_user, db)


@router_customers.put("/update")
def user_update(form: CustomersUpdate, db: Session = Depends(get_db),current_user: CustomersCurrent = Depends(get_current_active_user)) :
    if update_customers(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_customers.delete('/{id}',  status_code = 200)
def delete_user(id: int = 0,db: Session = Depends(get_db), current_user: CustomersCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return user_delete(id, db)