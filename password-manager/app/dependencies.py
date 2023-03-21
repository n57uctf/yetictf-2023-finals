import os

import psycopg2
from psycopg2.extras import DictCursor
import jwt
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(user=os.environ.get("DB_USER") or 'postgres',
                                           password=os.environ.get("DB_PASSWORD") or 'postgresql',
                                           host=os.environ.get("DB_HOST") or '127.0.0.1',
                                           port=os.environ.get("DB_PORT") or "5432",
                                           database=os.environ.get("DB_NAME") or "PasswordManager",
                                           cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        try:
            create_table_users_query = '''CREATE TABLE IF NOT EXISTS "User" (
                                          "@User" SERIAL PRIMARY KEY,
                                          "Username" TEXT NOT NULL,
                                          "Password" TEXT NOT NULL,
                                          "MasterPassword" TEXT NOT NULL
                                          );'''
            self.cursor.execute(create_table_users_query)

            create_table_storage_query = '''CREATE TABLE IF NOT EXISTS "Storage" (
                                          "@Record" SERIAL PRIMARY KEY,
                                          "Owner@" TEXT NOT NULL,
                                          "Password" TEXT NOT NULL,
                                          "Title" TEXT NOT NULL
                                          );'''
            self.cursor.execute(create_table_storage_query)

            create_table_links_query = '''CREATE TABLE IF NOT EXISTS "Links" (
                                          "@Link" SERIAL PRIMARY KEY,
                                          "LinkCode" TEXT NOT NULL,
                                          "Record@" INT REFERENCES "Storage"
                                          );'''
            self.cursor.execute(create_table_links_query)
            self.connection.commit()
            print("Таблицы успешно созданы")

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def execute(self, *args, **kwargs):
        try:
            self.cursor.execute(*args, **kwargs)
            return self.cursor
        except (Exception, psycopg2.Error) as error:
            raise HTTPException(404, str(error))


class Authentication:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def check_reg(self, username, password):
        is_registered = self.database.execute('''
        SELECT "@User", "Username", "Password"
        FROM "User"
        WHERE "Username"=%s''', (username,))
        result = is_registered.fetchall()
        self.database.connection.commit()
        try:
            for i in result:
                if i[2] == password:
                    return i
        except Exception as error:
            raise HTTPException(403, str(error))

    def get_auth_token(self, username, user_id):
        try:
            key = os.environ.get("JWT_KEY") or "0db120c4bfd93e453dea115cd9079d709f452adee19e9600eedb0953d599e1b1"
            encoded = jwt.encode({"username": username, "id": user_id}, key, algorithm="HS256")
            print(encoded)
            return encoded
        except Exception as error:
            raise HTTPException(403, str(error))

    def verify_auth_token(self, token):
        try:
            key = os.environ.get("JWT_KEY") or "0db120c4bfd93e453dea115cd9079d709f452adee19e9600eedb0953d599e1b1"
            return jwt.decode(token, key, algorithms=["HS256"])
        except Exception as error:
            raise HTTPException(403, str(error))


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


