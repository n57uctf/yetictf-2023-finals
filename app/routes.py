import hashlib

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import Database, JWTBearerAccess, Authentication
from app.models import CredentialModel, UserModel, AccessTokenModel, StorageModel, CreateStorageModel


router = APIRouter()


@router.post("/login", response_model=AccessTokenModel)
async def login(creds: CredentialModel, auth: Authentication = Depends(Authentication)):
    is_registered = auth.check_reg(creds.username, str(hashlib.sha256(creds.password.encode()).hexdigest()))
    if is_registered:
        return AccessTokenModel(token=auth.get_auth_token(is_registered[1], is_registered[0]))
    else:
        raise HTTPException(404, "User not found")


@router.post("/register", response_model=UserModel)
async def register(creds: CredentialModel, database: Database = Depends(Database)):
    cursor = database.execute('''
insert into "User" 
("Username", "Password", "MasterPassword") 
values (%s, %s, %s) 
returning "@User" as user_id, "Username" as username, "Password" as password, "MasterPassword" as masterpass
    ''', (creds.username, str(hashlib.sha256(creds.password.encode()).hexdigest()), "1233567"))
    user_creds = UserModel(**cursor.fetchone())
    database.connection.commit()
    return user_creds


@router.post("/storage", response_model=StorageModel)
async def create_password(storage_data: CreateStorageModel, jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
                          database: Database = Depends(Database)):
    cursor = database.execute('''
    insert into "Storage" 
    ("Password", "Owner@", "Title") 
    values (%s, %s, %s) 
    returning "@Record" as record_id, "Password" as password, "Owner@" as owner_username, "Title" as title
        ''', (storage_data.password, jwt["username"], storage_data.title))
    storage = StorageModel(**cursor.fetchone())
    database.connection.commit()
    return storage


@router.get("/storage")
async def read_password():
    pass


@router.get("/share")
async def share():
    ...


@router.get("/export")
async def export():
    ...
