CREATE TABLE IF NOT EXISTS UserT (
  _User serial PRIMARY KEY,
  Nickname text NOT NULL,
  Password text NOT NULL,
  PublicInfo text,
  PrivateInfo text,
  IsVip bool NOT NULL,
  image bytea,
  Additional jsonb
 );

CREATE TABLE IF NOT EXISTS GroupT (
	_Group serial PRIMARY KEY,
	Name text NOT NULL,
	Description text NOT NULL,
	IsPublic bool NOT NULL,
	Creator_ int NOT NULL REFERENCES UserT(_User)
);
CREATE TABLE IF NOT EXISTS GroupUser (
	User_ int NOT NULL REFERENCES UserT(_User),
	Group_ int NOT NULL REFERENCES GroupT(_Group)
);
CREATE TABLE IF NOT EXISTS Thread (
	_Thread serial PRIMARY KEY,
	Group_ int NOT NULL REFERENCES GroupT(_Group),
	Name text NOT NULL,
	Description text NOT NULL
);
CREATE TABLE IF NOT EXISTS Comment (
	_Comment serial PRIMARY KEY,
	User_ int NOT NULL REFERENCES UserT(_User),
	Thread_ int NOT NULL REFERENCES Thread(_Thread),
	Text text NOT NULL,
	_time text NOT NULL
);
