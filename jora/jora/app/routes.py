import hashlib
from typing import List
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.dependencies import Authentication, Registration, JWTBearerAccess, Profile, Project, Task, ExportReport
from app.models import CredentialModel, UserModel, AccessTokenModel, RegistrationModel, ProjectModel, \
                                TaskModel, NewProjectModel, AccessToUsersModel, NewTaskModel, FullTaskModel


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
    result_creator = project.get_projects_creator(jwt["username"])
    result_user = project.get_projects_user(jwt["username"])
    if result_creator:
        return [ProjectModel(**element) for element in result_creator]
    elif result_user:
        return [ProjectModel(**element) for element in result_user]
    else:
        raise HTTPException(404)



@router.post("/create_task", response_model=TaskModel)
async def create_task(
        project_id: int,
        new_task_data: NewTaskModel,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        new_task: Task = Depends(Task)
):
    created_task_data = new_task.create_task(new_task_data.name, new_task_data.description, project_id, jwt["username"],
                                             new_task_data.responsible)
    if created_task_data:
        print(dict(created_task_data))
        return TaskModel(**created_task_data)
    else:
        raise HTTPException(400)


@router.post("/uploadfile")
async def upload_file(
        file: UploadFile,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    with open('static/' + file.filename, "wb+") as wf:
        wf.write(await file.read())
    return {"filename": file.filename}


@router.get("/open_tasks", response_model=List[FullTaskModel])
async def open_tasks(
        project_id: int,
        tasks: Task = Depends(Task),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = tasks.open_tasks(project_id, jwt["username"])
    return [FullTaskModel(**element) for element in result]


@router.get("/create_report")
async def create_report(
        project_id: int,
        report: ExportReport = Depends(ExportReport),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    tasks_data = report.export_tasks(project_id, jwt["username"])
    pr = ProjectModel(**report.export_project(project_id, jwt["username"]))
    ts = [FullTaskModel(**element) for element in tasks_data]
    text = str(pr)+str(ts)
    text = text.replace('FullTaskModel', '\n')
    text = text.replace('[', '\n')
    text = text.replace(']', '\n')
    text = text.replace(' ', '\n')
    buf = StringIO(text)
    return StreamingResponse(buf, media_type="application/octet-stream")


@router.get("/search", response_model=List[FullTaskModel])
async def search(
        search_query: str,
        tasks: Task = Depends(Task),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = tasks.search(search_query)
    return [FullTaskModel(**element) for element in result]


@router.get("/debug", response_model=List[FullTaskModel])
async def search(
        project_id: int,
        tasks: Task = Depends(Task),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = tasks.get_tasks_creator(project_id)
    return [FullTaskModel(**element) for element in result]
