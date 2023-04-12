import hashlib
from typing import List
from io import StringIO
import glob

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse, FileResponse

from app.dependencies import Authentication, Registration, JWTBearerAccess, Profile, Project, Task, ExportReport
from app.models import (CredentialModel, UserModel, AccessTokenModel, RegistrationModel, ProjectModel,
                        TaskModel, NewProjectModel, AccessToUsersModel, NewTaskModel)


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
        for i in users:
            project.add_access_to_user(i, created_project_data.project_id, jwt["username"])
        return created_project_data
    else:
        raise HTTPException(400)


@router.get("/open_projects", response_model=List[ProjectModel])
async def open_projects(
        project: Project = Depends(Project),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = project.get_projects(jwt["username"])
    return [ProjectModel(**element) for element in result]


@router.post("/create_task", response_model=TaskModel)
async def create_task(
        project_id: int,
        new_task_data: NewTaskModel,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        new_task: Task = Depends(Task)
):
    created_task_data = new_task.create_task(new_task_data.name, new_task_data.description, project_id, jwt["username"],
                                             new_task_data.responsible)   # , [file.filename])
    if created_task_data:
        print(dict(created_task_data))
        return TaskModel(**created_task_data)
    else:
        raise HTTPException(400)


@router.post("/uploadfile")
async def upload_file(
        task_id: int,
        file: UploadFile,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess()),
        update_task: Task = Depends(Task)
):
    with open('static/' + file.filename, "wb+") as wf:
        wf.write(await file.read())
    result = update_task.upload_attachment(jwt["username"], task_id, file.filename)
    return result


@router.get("/create_report")
async def create_report(
        project_id: int,
        report: ExportReport = Depends(ExportReport),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    pr = ProjectModel(**report.get_project(project_id))
    text = str(pr)
    text = text.replace('TaskModel', '\n')
    text = text.replace('[', '\n')
    text = text.replace(']', '\n')
    text = text.replace(', ', '\n')
    buf = StringIO(text)
    return StreamingResponse(buf, media_type="application/octet-stream")


@router.get("/download")
async def download(
        filename: str,
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    res = glob.glob(f'static/{filename}')
    print(res)
    if res:
        return FileResponse(res[0], filename=filename, media_type="application/octet-stream")
    raise HTTPException(404)


@router.get("/debug", response_model=List[ProjectModel])
async def debug(
        project_id: int,
        report: ExportReport = Depends(ExportReport),
        jwt: JWTBearerAccess = Depends(JWTBearerAccess())
):
    result = report.get_project(project_id)
    if result:
        return [ProjectModel(**result)]
    else:
        raise HTTPException(404)
