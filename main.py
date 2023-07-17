from db import SessionLocal
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from models.users import Users
from routes import users, auth, orders, customers, products, expenses, backet, product_types
from db import Base, engine
import datetime

from routes.auth import get_password_hash

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eko zamin",
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)


app.include_router(
    router=orders.order_router,
    tags=["Orders bo'limi"],
    prefix='/orders'
)

app.include_router(
    router=customers.customers_router,
    tags=["Customers bo'limi"],
    prefix='/customers'
)

app.include_router(
    router=products.router_product,
    tags=["Products bo'limi"],
    prefix='/products'
)

app.include_router(
    router=product_types.product_type_router,
    tags=["Products_type bo'limi"],
    prefix='/product_type'
)


app.include_router(
    router=expenses.expenses_router,
    tags=["Expenses bo'limi"],
    prefix='/expenses'

)

app.include_router(
    router=backet.backet_router,
    tags=["Backet bo'limi"],
    prefix='/backet'
)


try:
  db=SessionLocal()
  new_user_db = Users(
    name='www',
    username='www',
    number='form.number',
    password=get_password_hash('111111'),
    roll='www',
    status=True,

  )
  db.add(new_user_db)
  db.commit()
  db.refresh(new_user_db)
except Exception :
  print(Exception)

