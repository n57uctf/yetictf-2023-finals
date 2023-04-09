from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: int
    username: str
    password: str
    info: str


class RegistrationModel(BaseModel):
    username: str
    password: str
    info: str


class CredentialModel(BaseModel):
    username: str
    password: str


class AccessTokenModel(BaseModel):
    token: str


class NewProjectModel(BaseModel):
    name: str
    description: str


class AccessToUsersModel(BaseModel):
    usernames: list[str]


class FullTaskModel(BaseModel):
    task_id: int
    name: str
    description: str
    attachments: list[str]  # | None
    responsible: str


class TaskModel(BaseModel):
    task_id: int
    name: str
    description: str
    attachments: list[str]
    responsible: str


class ProjectModel(BaseModel):
    project_id: int
    name: str
    description: str
    creator: bool
    tasks: list[TaskModel]
    type: str


class NewTaskModel(BaseModel):
    name: str
    description: str
    responsible: str
    # attachments: list[str]
