from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service.app.routes import router
from service.app.dependencies import Database

app = FastAPI()
app.include_router(router)
Database().create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)