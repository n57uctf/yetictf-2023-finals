package main

import (
	"database/sql"
	"fmt"
	"log"
)

type DB struct {
	SQL  *sql.DB
	Path string
}

func CreateDB(path string) (DB, error) {
	sqlDB, err := sql.Open("sqlite3", path)
	if err != nil {
		return DB{}, err
	}
	schemaSQL := "CREATE TABLE IF NOT EXISTS `users` (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `username` TEXT, `password` TEXT, `role` INTEGER);CREATE TABLE IF NOT EXISTS `history` (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `temp` INTEGER, `comment` TEXT, `timestamp` INTEGER, `user_id` INTEGER, `username` TEXT);"
	_, err = sqlDB.Exec(schemaSQL)
	if err != nil {
		return DB{}, err
	}
	rows, err := sqlDB.Query("SELECT count(*) FROM `users` WHERE `username`='admin';")
	if err != nil {
		return DB{}, err
	}
	var count int
	for rows.Next() {
		err = rows.Scan(&count)
		if err != nil {
			return DB{}, err
		}
	}
	if count == 0 {
		insertDefaultUserSQL := "INSERT INTO `users` (`username`, `password`, `role`) VALUES ('admin', 'admin', 1);"
		_, err = sqlDB.Exec(insertDefaultUserSQL)
	}
	return DB{sqlDB, path}, err
}

func (db *DB) CountUser(username string) (int, error) {
	rows, err := db.SQL.Query(fmt.Sprintf("SELECT count(*) FROM `users` WHERE `username`='%v';", username))
	var count int
	for rows.Next() {
		err = rows.Scan(&count)
		if err != nil {
			return -1, err
		}
	}
	return count, nil
}

func (db *DB) GetAllHistoryMarks() ([]CCR, error) {
	result := make([]CCR, 0)
	rows, err := db.SQL.Query("SELECT `temp`, `comment`, `timestamp`, `user_id`, `username` FROM `history` LIMIT 10;")
	for rows.Next() {
		tmp := CCR{}
		err = rows.Scan(&tmp.SettedTemperature, &tmp.Comment, &tmp.UnixNano, &tmp.UserID, &tmp.UserName)
		if err != nil {
			continue
		}
		result = append(result, tmp)
	}
	return result, nil
}

func (db *DB) GetAllHistoryMarksForUser(username string) ([]CCR, error) {
	result := make([]CCR, 0)
	rows, err := db.SQL.Query(fmt.Sprintf("SELECT `temp`, `comment`, `timestamp`, `user_id`, `username` FROM `history` WHERE `username`='%v';", username))
	for rows.Next() {
		tmp := CCR{}
		err = rows.Scan(&tmp.SettedTemperature, &tmp.Comment, &tmp.UnixNano, &tmp.UserID, &tmp.UserName)
		if err != nil {
			continue
		}
		result = append(result, tmp)
	}
	return result, nil
}

func (db *DB) CreateHistoryMark(ccr CCR) error {
	insertHistoryMark := fmt.Sprintf("INSERT INTO `history` (`temp`,`comment`,`timestamp`,`user_id`,`username`) VALUES ('%v', '%v', '%v', '%v', '%v')", ccr.SettedTemperature, ccr.Comment, ccr.UnixNano, ccr.UserID, ccr.UserName)
	_, err := db.SQL.Exec(insertHistoryMark)
	return err
}

func (db *DB) Close() error {
	return db.SQL.Close()
}

func (db *DB) GetUser(username string) (User, error) {
	getUserSQL := fmt.Sprintf("SELECT `username`,`password`,`role`,`id` FROM `users` WHERE `username`='%v';", username)
	rows, err := db.SQL.Query(getUserSQL)
	var user User
	for rows.Next() {
		err = rows.Scan(&user.Username, &user.Password, &user.Role, &user.ID)
		if err != nil {
			log.Println(err)
			return user, err
		}
		log.Println(user)
	}
	return user, nil
}

func (db *DB) CreateUser(username, password string, role int) error {
	insertUserSQL := fmt.Sprintf("INSERT INTO `users` (`username`, `password`, `role`) VALUES ('%v', '%v', %v);", username, password, role)
	_, err := db.SQL.Exec(insertUserSQL)
	return err
}
