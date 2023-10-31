from fastapi import FastAPI

from src.auth.routers import router as user_router

app = FastAPI()
app.include_router(
    user_router,
    prefix='/users',
    tags=['users']
)


@app.get('/')
def hello_world():
    return {'message': 'hello world'}
