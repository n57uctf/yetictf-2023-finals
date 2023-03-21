from fastapi import FastAPI

from app.routes import router
from app.dependencies import Database

app = FastAPI()
app.include_router(router)
Database().create_tables()
