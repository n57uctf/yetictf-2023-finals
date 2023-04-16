CREATE TABLE users (
	id Int not null auto_increment primary key,
	username varchar(100),
	email varchar(255),
	first_name varchar(100),
	last_name varchar(100),
	patronymic varchar(100),
	password varchar(255),
	balance Int,
	account_number Int
);
INSERT users (username, email, first_name, last_name, patronymic, password, balance, account_number) VALUES ('Cheker', 'chek@mail', 'NSTU', 'DepartamentDI', 'YetiCTF2023', '$2a$10$bdipdis6nl/UdhX0E/bILunzekKa.7kF99h4m4lAxjyr731.Ps7tC', 100000, 1604);
CREATE TABLE roles (
	id Int not null auto_increment primary key,
	name varchar(100)
);
INSERT roles (name) VALUES ('ROLE_USER');
INSERT roles (name) VALUES ('ROLE_ADMIN');
CREATE TABLE user_roles (
    user_id INT(11) NOT NULL,
    role_id INT(11) NOT NULL,
    PRIMARY KEY (user_id, role_id),
    INDEX user_id (user_id),
    INDEX role_id (role_id),
    CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_roles FOREIGN KEY (role_id)
        REFERENCES roles (id) ON DELETE CASCADE
);
INSERT user_roles (user_id, role_id) VALUES (1, 2);
CREATE TABLE transfer(
id Int not null auto_increment primary key,
account_number_from Int,
account_number_to Int,
amount Int,
comments varchar(255)
);
