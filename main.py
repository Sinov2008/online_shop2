from db import SessionLocal
from fastapi import FastAPI
# from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session


from routes import   users,auth,backet,products,expenses,customers,orders,incomes,product_types
from db import Base, engine
import datetime



Base.metadata.create_all(bind=engine)

app=FastAPI(
	title="fast api",
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
	return {"message": "welcome"}


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
	backet.router_backet,
	prefix='/backet',
	tags=['backet section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)


app.include_router(
	products.router_product,
	prefix='/products',
	tags=['products section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	expenses.router_expenses,
	prefix='/expenses',
	tags=['expenses section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	customers.router_customers,
	prefix='/customers',
	tags=['customers section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)


app.include_router(
	orders.router_order,
	prefix='/orders',
	tags=['orders section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)


app.include_router(
	incomes.router_incomes,
	prefix='/incomes',
	tags=['incomes section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	product_types.router_product_types,
	prefix='/product_types',
	tags=['product_types section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)
