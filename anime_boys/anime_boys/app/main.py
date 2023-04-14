import starlette.status as status
import datetime
import base64
import io
import logging
import time
import uvicorn
import tempfile
import os
from fastapi import FastAPI,Request, Form, Cookie, File, UploadFile, Path, HTTPException
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse,HTMLResponse,RedirectResponse, Response
from app.secure import *
from app.sqldb import *
from app.models import *
from io import BytesIO

time.sleep(2)


logging.basicConfig(level=logging.INFO)


db = SQLDB({
            'host': 'db',
            'port': '5432',
            'database': 'postgres',
            'user': 'postgres',
            'password': 'qweasdzxc1'
        })
db.execute('create_db').none()
app = FastAPI(docs_url=None, redoc_url=None)
from app.routes import *
