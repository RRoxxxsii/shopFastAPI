from fastapi import FastAPI

from src.auth.routers import router as user_router
from src.partners.routers import router as partner_router

app = FastAPI()
app.include_router(
    user_router,
    prefix='/users',
    tags=['users']
)

app.include_router(
    partner_router,
    prefix='/partners',
    tags=['partners']
)


@app.get('/')
def hello_world():
    return {'message': 'hello world'}
