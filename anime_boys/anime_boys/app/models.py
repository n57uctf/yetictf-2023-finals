from app.main import *
from typing import Optional
from pydantic import Field, Required

class User(BaseModel):
    user_id : int
    nickname : str
    password : str
    publicinfo : str | None
    privateinfo : str | None
    isvip : bool
    additional : Json | None
    img : memoryview | None
    class Config:
        arbitrary_types_allowed = True

class UserLogin(BaseModel):
    user_id : int
    nickname : str
    password : str

class Group(BaseModel):
    group_id : int
    name : str
    description : str
    ispublic : bool
    creator : int
    creator_name : str | None
    number_of_threads : int | None = 0
    number_of_comments : int | None = 0

class GroupUser(BaseModel):
    user_id : int
    group_id : int
    group_name: str | None

class Thread(BaseModel):
    thread_id : int
    group_id : int
    group_name : str | None
    name : str
    description : str
    number_of_comments : int | None = 0
    last_comment_username : str | None
    last_comment_userid : int | None

class Comment(BaseModel):
    comment_id : int
    user_id : int | None
    thread_id : int
    text : str | None
    name : str | None
    isvip : bool | None
    img : memoryview | None
    time : str | None
    class Config:
        arbitrary_types_allowed = True