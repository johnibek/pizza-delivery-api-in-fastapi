from fastapi import FastAPI
from .routers import auth_routes, order_routes, user_routes
from .database import engine
from .models import Base

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pizza Delivery API")

app.include_router(auth_routes.auth_router)
app.include_router(order_routes.order_router)
app.include_router(user_routes.user_router)

@app.get("/")
async def hello():
    return {'message': 'Hello world'}
