import hashlib
from typing import List
from io import BytesIO
import random
import string
import ctypes
import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.dependencies import Database, JWTBearerAccess, Authentication, Link, ExportStorage
from app.models import CredentialModel, UserModel, AccessTokenModel, StorageModel, CreateStorageModel, ShareLinkModel, \
    ExportLinkModel, RegisteredUsersModel, DecryptModel, DecryptedDataModel

router = APIRouter(prefix="/api")


@router.get("/get_users", response_model=List[RegisteredUsersModel])
async def get_last_10_users(
        database: Database = Depends(Database)
):
    cursor = database.execute('''
        select "Username" as username
        from "User"
        order by "@User" desc
        limit 10''')
    return [RegisteredUsersModel(username=element[0]) for element in cursor.fetchall()]


@router.post("/login", response_model=AccessTokenModel)
async def login(
        creds: CredentialModel,
        auth: Authentication = Depends(Authentication)
):
    is_registered = auth.check_reg(creds.username, str(hashlib.sha256(creds.password.encode()).hexdigest()))
    if is_registered:
        return AccessTokenModel(token=auth.get_auth_token(is_registered[1], is_registered[0]))
    else:
        raise HTTPException(404, "User not found")


@router.get("/profile", response_model=UserModel)
async def profile_info(
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        database: Database = Depends(Database)
):
    cursor = database.execute('''
        select "@User" as user_id, "Username" as username, "Password" as password, "MasterPassword" as masterpass
        from "User"
        where "@User"=%s''', (jwt['id'],))
    return UserModel(**cursor.fetchone())


@router.post("/register", response_model=UserModel)
async def register(
        creds: CredentialModel,
        database: Database = Depends(Database)
):
    random_masterpass = ''.join(random.choice(string.digits) for i in range(32))
    cursor = database.execute('''
        insert into "User" 
        ("Username", "Password", "MasterPassword") 
        values (%s, %s, %s) 
        returning "@User" as user_id, "Username" as username, "Password" as password, "MasterPassword" as masterpass
            ''', (creds.username, str(hashlib.sha256(creds.password.encode()).hexdigest()), random_masterpass))
    user_creds = UserModel(**cursor.fetchone())
    database.connection.commit()
    return user_creds


@router.post("/storage", response_model=StorageModel)
async def create_password(
        storage_data: CreateStorageModel,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        database: Database = Depends(Database)
):
    cursor = database.execute('''
        insert into "Storage" 
        ("Password", "Owner@", "Title") 
        values (%s, %s, %s) 
        returning "@Record" as record_id, "Password" as password, "Owner@" as owner_username, "Title" as title
            ''', (storage_data.password, jwt["username"], storage_data.title))
    storage = StorageModel(**cursor.fetchone())
    database.connection.commit()
    return storage


@router.get("/storage", response_model=List[StorageModel])
async def read_password(
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        database: Database = Depends(Database)
):
    cursor = database.execute('''
        select "@Record" as record_id, "Password" as password, "Owner@" as owner_username, "Title" as title 
        from "Storage"
        where "Owner@"=%s''', (jwt["username"],))
    return [StorageModel(**element) for element in cursor.fetchall()]


@router.get("/share", response_model=ShareLinkModel)
async def share(
        record_id: int,
        link: Link = Depends(Link),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    return ShareLinkModel(**link.create_link(jwt["username"], record_id))


@router.get("/shared_link", response_model=CreateStorageModel)
async def shared_link(
        shared_password_link: str,
        link: Link = Depends(Link)
):
    return CreateStorageModel(**link.check_link(shared_password_link))


@router.get("/export", response_model=ExportLinkModel)
async def export(
        username: str,
        storage: ExportStorage = Depends(ExportStorage)
):
    return ExportLinkModel(link=storage.create_link(username))


@router.post("/decrypt", response_model=DecryptedDataModel)
async def decrypt(
        data: DecryptModel,
        storage: ExportStorage = Depends(ExportStorage)
):
    # key = storage.key_gen(data.master_password)
    decrypt_data = storage.encrypt(data.data.encode('UTF-8'), data.master_password.encode('UTF-8'))
    return DecryptedDataModel(data=str(decrypt_data))


@router.get("/file")
async def download_file(
        link: str,
        storage: ExportStorage = Depends(ExportStorage)
):
    username = link.split("/").pop()
    data_to_export = storage.create_export(username)
    master_password = storage.get_master_password(username)
    text = """Data format: {"password":<user-password>, "title":<service-title>}{<next record>}"""
    value = "\n".join(': '.join(password_title) for password_title in data_to_export)
    # key = storage.key_gen(master_password[0])
    key = master_password[0]
    buf = BytesIO(storage.encrypt((text+value).encode('UTF-8'), key.encode('UTF-8')))
    return StreamingResponse(buf, media_type="application/octet-stream")
