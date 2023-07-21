from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user
Base.metadata.create_all(bind=engine)
from functions.orders import one_order, all_orders, update_order, create_order, order_delete,order_current
from schemas.users import UserBase,UserCreate,UserUpdate,UserCurrent

router_order = APIRouter()



@router_order.post('/add', )
def add_user(form: UserCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_order(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_order.get('/',  status_code = 200)
def get_users(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_order(id, db)
    else :
        return all_orders(search, status,roll, page, limit, db)

@router_order.get('/user',  status_code = 200)
def get_user_current(db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return order_current(current_user, db)


@router_order.put("/update")
def user_update(form: UserUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_order(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_order.delete('/{id}',  status_code = 200)
def delete_user(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return order_delete(id, db)