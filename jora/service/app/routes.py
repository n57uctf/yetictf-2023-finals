import hashlib
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from service.app.dependencies import Authentication, Registration, JWTBearerAccess, Profile, Project, Task
from service.app.models import CredentialModel, UserModel, AccessTokenModel, RegistrationModel, ProjectModel, TaskModel, NewProjectModel, AccessToUsersModel, NewTaskModel


router = APIRouter(prefix="/api")


@router.post("/register", response_model=UserModel)
async def register(
        creds: RegistrationModel,
        reg: Registration = Depends(Registration)
):
    return(UserModel(
        **reg.register_user(creds.username,
                            str(hashlib.sha256(creds.password.encode()).hexdigest()),
                            creds.info)
    ))


@router.post("/login", response_model=AccessTokenModel)
async def login(
        creds: CredentialModel,
        auth: Authentication = Depends(Authentication)
):
    is_registered = auth.check_reg(creds.username, str(hashlib.sha256(creds.password.encode()).hexdigest()))
    if is_registered:
        return AccessTokenModel(token=auth.get_auth_token(is_registered[0]))
    else:
        raise HTTPException(400, "Not correct username/password")


@router.get("/profile", response_model=UserModel)
async def profile_data(
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        profile_info: Profile = Depends(Profile)
):
    return UserModel(**profile_info.get_profile_info(jwt['username']))


@router.post("/create_project", response_model=ProjectModel)
async def create_project(
        users: list,
        new_project_data: NewProjectModel,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        project: Project = Depends(Project)
):
    created_project_data = project.create_project(new_project_data.name, new_project_data.description, jwt["username"])
    if created_project_data:
        created_project_data = ProjectModel(**created_project_data)
        if users[0] != '':
            for i in users:
                project.add_access_to_user(i, created_project_data.project_id, jwt["username"])
            return created_project_data
        return created_project_data
    else:
        raise HTTPException(400)


@router.post("/add_user_to_project", response_model=AccessToUsersModel)
async def add_user_to_project(
        users: list,
        project_id: int,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        project: Project = Depends(Project)
):
    for i in users:
        project.add_access_to_user(str(i), project_id, jwt["username"])
    return AccessToUsersModel(usernames=users)


@router.get("/open_projects", response_model=List[ProjectModel])
async def open_projects(
        project: Project = Depends(Project),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = project.get_projects(jwt["username"])
    if result:
        return (ProjectModel(**element) for element in result)
    else:
        raise HTTPException(400)


@router.post("/create_task", response_model=TaskModel)
async def create_task(
        project_id: int,
        new_task_data: NewTaskModel,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        new_task: Task = Depends(Task)
):
    created_task_data = new_task.create_task(new_task_data.name, new_task_data.description, new_task_data.attachments,
                                             project_id, jwt["username"], new_task_data.responsible)
    if created_task_data:
        print(dict(created_task_data))
        return TaskModel(**created_task_data)
    else:
        raise HTTPException(400)


@router.get("/open_tasks", response_model=List[TaskModel])
async def open_tasks(
        project_id: int,
        tasks: Task = Depends(Task),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = tasks.open_tasks(project_id, jwt["username"])
    if result:
        return (TaskModel(**element) for element in result)
    else:
        raise HTTPException(400)


@router.post("/create_report")
async def create_report(
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    ...


@router.get("/search", response_model=List[TaskModel])
async def search(
        search_query: str,
        tasks: Task = Depends(Task),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = tasks.search(search_query)
    if result:
        return (TaskModel(**element) for element in result)
    else:
        raise HTTPException(400)


@router.get("/debug", response_model=List[TaskModel])
async def search(
        project_id: int,
        tasks: Task = Depends(Task),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = tasks.get_tasks(project_id)
    if result:
        return (TaskModel(**element) for element in result)
    else:
        raise HTTPException(400)
