import hashlib
import os

import psycopg2
from psycopg2.extras import DictCursor
import jwt
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(user=os.environ.get("POSTGRES_USER") or 'postgres',
                                           password=os.environ.get("POSTGRES_PASSWORD") or 'postgresql' or 'postgres',
                                           host=os.environ.get("POSTGRES_HOST") or '127.0.0.1',
                                           port=5432,
                                           database=os.environ.get("POSTGRES_DB") or "PasswordManager",
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

        except:
            raise HTTPException(500)

    def execute(self, *args, **kwargs):
        try:
            self.cursor.execute(*args, **kwargs)
            return self.cursor
        except:
            raise HTTPException(500)


class Authentication:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def check_reg(self, username, password):
        try:
            is_registered = self.database.execute('''
                SELECT "@User", "Username", "Password"
                FROM "User"
                WHERE "Username"=%s''', (username,))
            result = is_registered.fetchall()
            self.database.connection.commit()
            for i in result:
                if i[2] == password:
                    return i
        except:
            raise HTTPException(403)

    def get_auth_token(self, username, user_id):
        try:
            key = os.environ.get("JWT_KEY") or "0db120c4bfd93e453dea115cd9079d709f452adee19e9600eedb0953d599e1b1"
            encoded = jwt.encode({"username": username, "id": user_id}, key, algorithm="HS256")
            return encoded
        except:
            raise HTTPException(403)

    def verify_auth_token(self, token):
        try:
            key = os.environ.get("JWT_KEY") or "0db120c4bfd93e453dea115cd9079d709f452adee19e9600eedb0953d599e1b1"
            return jwt.decode(token, key, algorithms=["HS256"])
        except:
            raise HTTPException(403)


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


class Link:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def create_link(self, username, record_id):
        try:
            str2hash = f"{username}{record_id}"
            link = hashlib.md5(str2hash.encode())
            add_link = self.database.execute('''
                    insert into "Links"
                    ("LinkCode", "Record@")
                    values (%s, %s)
                    returning "LinkCode" as link
                    ''', (link.hexdigest(), record_id))
            link_from_db = add_link.fetchone()
            self.database.connection.commit()
            return link_from_db
        except:
            raise HTTPException(400)

    def check_link(self, link):
        try:
            check_link_db = self.database.execute('''
                    SELECT "Record@"
                    FROM "Links"
                    WHERE "LinkCode"=%s''', (link,))
            record_id = check_link_db.fetchone()
            if record_id:
                get_password = self.database.execute('''
                    SELECT "Password" as password, "Title" as title
                    FROM "Storage"
                    WHERE "@Record"=%s''', (record_id[0],))
                return get_password.fetchone()
        except:
            raise HTTPException(400)


class ExportStorage:
    def __init__(self, database: Database = Depends(Database)):
        self.database = database

    def create_link(self, username):
        try:
            link = f"/export_backup/{username}"
            return link
        except:
            raise HTTPException(404)

    def create_export(self, username):
        try:
            check_user = self.database.execute('''
                    SELECT "Title" as title, "Password" as password
                    FROM "Storage"
                    WHERE "Owner@"=%s''', (username,))
            data_from_storage = check_user.fetchall()
            self.database.connection.commit()
            return data_from_storage
        except:
            raise HTTPException(500)

    def get_master_password(self, username):
        try:
            master_pass = self.database.execute('''
            SELECT "MasterPassword"
                    FROM "User"
                    WHERE "Username"=%s''', (username,))
            data_from_storage = master_pass.fetchone()
            self.database.connection.commit()
            return data_from_storage
        except:
            raise HTTPException(500)

    def key_gen(self, key):
        new_key = ''
        for i in range(8):
            for j in range(4):
                new_key += key[i * 4 + 3 - j]
        print(new_key)
        return new_key

    def encrypt(self, text, key):
        new_text = ''
        key = self.key_gen(key)
        for i in range(len(text)):
            new_text += chr(ord(text[i]) ^ ord(key[i % 32]))
        return new_text

