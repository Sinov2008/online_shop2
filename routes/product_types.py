from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user
Base.metadata.create_all(bind=engine)
from functions.product_types import one_product_types,  update_product_types, create_product_types, product_types_delete,all_product_types
from schemas.users import UserBase,UserCreate,UserUpdate,UserCurrent

router_product_types = APIRouter()



@router_product_types.post('/add', )
def add_product_types(form: UserCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_product_types(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_product_types.get('/',  status_code = 200)
def get_product_types(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_product_types(id, db)
    else :
        return all_product_types(search, status, page, limit, db)

@router_product_types.get('/user',  status_code = 200)
def get_product_typesr_current(db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return all_product_types(current_user, db)


@router_product_types.put("/update")
def product_types_update(form: UserUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_product_types(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_product_types.delete('/{id}',  status_code = 200)
def delete_product_types(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return product_types_delete(id, db)