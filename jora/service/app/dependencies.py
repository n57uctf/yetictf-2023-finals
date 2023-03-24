import hashlib
import os
import jwt

import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(user=os.environ.get("POSTGRES_USER") or 'postgres',
                                           password=os.environ.get("POSTGRES_PASSWORD") or 'postgresql',
                                           host=os.environ.get("POSTGRES_HOST") or '127.0.0.1',
                                           port=5432,
                                           database=os.environ.get("POSTGRES_DB") or "Jora",
                                           cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        try:
            create_tables = '''CREATE TABLE IF NOT EXISTS "User" (
                                          "@User" SERIAL PRIMARY KEY,
                                          "Username" TEXT NOT NULL,
                                          "Password" TEXT NOT NULL,
                                          "Info" TEXT,
                                          CONSTRAINT username_unique UNIQUE ("Username")
                                          );
                                CREATE TABLE IF NOT EXISTS "Project" (
                                          "@Project" SERIAL PRIMARY KEY,
                                          "Name" TEXT NOT NULL,
                                          "Description" TEXT NOT NULL,
                                          "Creator@" INT REFERENCES "User"
                                          );
                                CREATE TABLE IF NOT EXISTS "Task" (
                                          "@Task" SERIAL PRIMARY KEY,
                                          "Name" TEXT NOT NULL,
                                          "Description" TEXT NOT NULL,
                                          "Attachments" text[] NOT NULL,
                                          "Project@" INT REFERENCES "Project",
                                          "Responsible@" INT REFERENCES "User"
                                          );
                                CREATE TABLE IF NOT EXISTS "UserProject" (
                                          "User@" INT REFERENCES "User",
                                          "Project@" INT REFERENCES "Project"
                                          );'''
            self.cursor.execute(create_tables)
            self.connection.commit()
        except:
            raise HTTPException(500)

    def execute(self, *args, **kwargs):
        try:
            self.cursor.execute(*args, **kwargs)
            return self.cursor
        except:
            raise HTTPException(500)


class Registration:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def register_user(self, username, password, info):
        try:
            registration = self.database.execute('''
            insert into "User" ("Username", "Password", "Info") values (%s, %s, %s) 
            returning "@User" as user_id, "Username" as username, "Password" as password, "Info" as info
            ''', (username, password, info))
            user_creds = registration.fetchone()
            self.database.connection.commit()
            return user_creds
        except (Exception, Error) as error:
            raise HTTPException(400, f"{error}")


class Authentication:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def check_reg(self, username, password):
        try:
            is_registered = self.database.execute('''
                SELECT "Username", "Password"
                FROM "User"
                WHERE "Username"=%s''', (username,))
            result = is_registered.fetchone()
            self.database.connection.commit()
            if result[1] == password:
                return result
        except:
            raise HTTPException(400, "Not correct username/password")

    def get_auth_token(self, username):
        try:
            key = os.environ.get("JWT_KEY") or "e026b52d5b14caf488b7f4eb0445c05b69c91c76"
            encoded = jwt.encode({"username": username}, key, algorithm="HS256")
            return encoded
        except (Exception, Error) as error:
            raise HTTPException(500, f"{error}")

    def verify_auth_token(self, token):
        try:
            key = os.environ.get("JWT_KEY") or "e026b52d5b14caf488b7f4eb0445c05b69c91c76"
            return jwt.decode(token, key, algorithms=["HS256"])
        except (Exception, Error) as error:
            raise HTTPException(400, f"{error}")


class JWTBearerAccess(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request, auth: Authentication = Depends(Authentication)) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(404, 'CredentialsNotFound')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(404, 'SchemeTypeError')
        return auth.verify_auth_token(credentials.credentials)


class Profile:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def get_profile_info(self, username):
        cursor = self.database.execute('''
                select "@User" as user_id, "Username" as username, "Password" as password, "Info" as info
                from "User"
                where "Username"=%s''', (username,))
        return cursor.fetchone()


class Project:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def create_project(self, name, description, username):
        is_project_name = self.database.execute('''
            with get_user as (select "@User" as user_id from "User" where "Username"=%s)
            select "Name" from "Project" 
            where "Name"=%s and "Creator@"=(select user_id from get_user limit 1)''', (username, name))
        if not is_project_name.fetchone():
            try:
                new_project = self.database.execute('''
                    with get_user as (select "@User" as user_id from "User" where "Username"=%s)
                    insert into "Project" ("Name", "Description", "Creator@") 
                    values (%s, %s, (select user_id from get_user limit 1)) 
                    returning "@Project" as project_id, "Name" as name, "Description" as description
                    ''', (username, name, description))
                project_data = new_project.fetchone()
                self.database.connection.commit()
                print(project_data)
                return project_data
            except (Exception, Error) as error:
                raise HTTPException(500, f"{error}")

    def add_access_to_user(self, username, project_id, creator):
        check_admin = self.database.execute('''
        with get_admin as (select "Creator@" as creator_id from "Project" where "@Project"=%s)
        select "Username" from "User" where "@User"=(select creator_id from get_admin limit 1)''', (project_id,))
        if check_admin.fetchone()[0] == creator:
            is_user_has_access = self.database.execute('''
                with get_user as (select "@User" as user_id from "User" where "Username"=%s)
                select "User@" from "UserProject" 
                where "User@"=(select user_id from get_user limit 1) and "Project@"=%s''', (username, project_id))
            if not is_user_has_access.fetchone():
                new_access = self.database.execute('''
                    with get_user as (select "@User" as user_id from "User" where "Username"=%s)
                    insert into "UserProject" ("User@", "Project@") 
                    values ((select user_id from get_user limit 1), %s) 
                    returning "User@" as user_id, "Project@" as project_id''', (username, project_id))
                project_access_data = new_access.fetchone()
                self.database.connection.commit()
                print(project_access_data)
                return project_access_data
            else:
                raise HTTPException(400, "User already has access")
        else:
            raise HTTPException(400, "Not creator of the project")

    def who_has_access(self, project_id):
        ...

    def get_project_id(self, project_name, creator):
        project_id = self.database.execute('''
        with get_user as (select "@User" as user_id from "User" where "Username"=%s)
        select "@Project" from "Project" 
        where "Name"=%s and "Creator@"=(select user_id from get_user limit 1)
        ''', (creator, project_name))
        return project_id.fetchone()[0]

    def get_project(self, project_name, creator_username):
        project = self.database.execute('''
        with get_user as (select "@User" as user_id from "User" where "Username"=%s)
        select "@Project" as project_id, "Name" as name, "Description" as description from "Project" 
        where "Name"=%s and "Creator@"=(select user_id from get_user limit 1)
        ''', (creator_username, project_name))
        return project.fetchone()

    def get_projects(self, creator_username):
        projects = self.database.execute('''
                with get_user as (select "@User" as user_id from "User" where "Username"=%s)
                select "@Project" as project_id, "Name" as name, "Description" as description from "Project" 
                where "Creator@"=(select user_id from get_user limit 1)
                ''', (creator_username,))
        return projects.fetchall()


class Task:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def create_task(self, name, description, attachments, project_id, creator_username, responsible_username):
        is_admin = self.database.execute('''
            with get_admin as (select "Creator@" as creator_id from "Project" where "@Project"=%s)
            select "Username" from "User" where "@User"=(select creator_id from get_admin limit 1)''', (project_id,))
        print(name, description, attachments, project_id, creator_username, responsible_username)
        if is_admin.fetchone()[0] == creator_username:
            is_task_name = self.database.execute('''
                select "Name" from "Task" 
                where "Name"=%s and "Project@"=%s''', (name, project_id))
            if not is_task_name.fetchone():
                is_respons_in_project = self.database.execute('''
                    with get_user as (select "@User" as user_id from "User" where "Username"=%s)
                    select "User@" from "UserProject" 
                    where "User@"=(select user_id from get_user limit 1) and "Project@"=%s
                    ''', (responsible_username, project_id))
                if is_respons_in_project.fetchone():
                    try:
                        new_task = self.database.execute('''
                                    with get_user as (select "@User" as user_id from "User" where "Username"=%s)
                                    insert into "Task" ("Name", "Description", "Attachments", "Project@", "Responsible@") 
                                    values (%s, %s, %s, %s, (select user_id from get_user limit 1)) 
                                    returning "Name" as name, "Description" as description, "Attachments" as attachments
                                    ''', (responsible_username, name, description, attachments, project_id))
                        task_data = dict(new_task.fetchone())
                        task_data.update({"responsible": responsible_username})
                        self.database.connection.commit()
                        return task_data
                    except (Exception, Error) as error:
                        raise HTTPException(500, f"{error}")
                else:
                    raise HTTPException(400, "Responsible user is not in the project")
            else:
                raise HTTPException(400, "There is already task with this name")
        else:
            raise HTTPException(400, "Not creator of the project")

    def reassign_task(self, name, project_id, responsible_username):
        ...

    def open_task(self, name, project_id, responsible_username):
        ...


class Debug:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database
