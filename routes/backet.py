from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user
Base.metadata.create_all(bind=engine)
from functions.backet import one_backet, all_backet, update_backet, create_backet, backet_delete,backet_current
from schemas.backet import BacketBase,BacketCreate,BacketUpdate,BacketCurrent


router_backet = APIRouter()



@router_backet.post('/add', )
def add_backet(form: BacketCreate, db: Session = Depends(get_db),current_user: BacketCurrent = Depends(get_current_active_user) ) : #
    if create_backet(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_backet.get('/',  status_code = 200)
def get_backet(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: backet_current = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_backet(id, db)
    else :
        return all_backet(search, status, page, limit, db)

@router_backet.get('/user',  status_code = 200)
def get_backet_current(db: Session = Depends(get_db),current_user: backet_current = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return backet_current(current_user, db)


@router_backet.put("/update")
def backet_update(form: BacketUpdate, db: Session = Depends(get_db),current_user: backet_current = Depends(get_current_active_user)) :
    if update_backet(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



@router_backet.delete('/{id}',  status_code = 200)
def delete_backet(id: int = 0,db: Session = Depends(get_db), current_user: backet_current = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return backet_delete(id, db)
    