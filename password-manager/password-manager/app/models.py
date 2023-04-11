from pydantic import BaseModel


class CredentialModel(BaseModel):
    username: str
    password: str


class UserModel(BaseModel):
    user_id: int
    username: str
    password: str
    masterpass: str


class AccessTokenModel(BaseModel):
    token: str


class StorageModel(BaseModel):
    record_id: int
    password: str
    owner_username: str
    title: str


class CreateStorageModel(BaseModel):
    password: str
    title: str


class ShareLinkModel(BaseModel):
    link: str


class ExportLinkModel(BaseModel):
    link: str


class RegisteredUsersModel(BaseModel):
    username: str


class DecryptModel(BaseModel):
    master_password: str
    data: str


class DecryptedDataModel(BaseModel):
    data: str
