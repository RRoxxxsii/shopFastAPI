from fastapi import FastAPI
from sqladmin import Admin

from src.infrastructure.admin import setup_admin_models
from src.infrastructure.database import engine
from src.presentation.api.controllers.v1.auth import router as user_router
from src.presentation.api.controllers.v1.item import router as item_router
from src.presentation.api.controllers.v1.partner import router as partner_router

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(partner_router, prefix="/partners", tags=["partners"])
app.include_router(item_router, prefix="/items", tags=["items"])


admin = Admin(app, engine)
setup_admin_models(admin)


@app.get("/")
def hello_world():
    return {"message": "hello world"}
