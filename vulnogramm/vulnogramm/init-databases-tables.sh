#!/bin/bash

set -e
psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER --dbname $POSTGRES_DB -w <<-EOSQL
CREATE TABLE IF NOT EXISTS "Post"
(
	"Id" serial PRIMARY KEY,
	"Owner" text NOT NULL,
	"Subscript" text NOT NULL,
	"PhotoForAll" text NOT NULL
);

CREATE TABLE IF NOT EXISTS "User"
(
	"Id" integer NOT NULL,
	"Login" text NOT NULL,
	"Password" text NOT NULL,
	CONSTRAINT "PK_User" PRIMARY KEY ("Id"),
	CONSTRAINT "User_Login_key" UNIQUE ("Login")
);
EOSQL
