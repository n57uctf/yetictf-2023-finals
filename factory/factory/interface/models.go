package main

import (
	"github.com/golang-jwt/jwt/v5"
	_ "github.com/mattn/go-sqlite3"
)

type Claims struct {
	jwt.RegisteredClaims
	Username string `json:"username"`
	Role     int    `json:"role"`
}

type CCR struct {
	SettedTemperature int    `json:"set_temperature"`
	Comment           string `json:"comment"`
	UnixNano          int64  `json:"nano_timestamp"`
	UserID            int    `json:"user_id"`
	UserName          string `json:"username"`
}

type User struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
	Role     int    `json:"int"`
}

type Credentials struct {
	Password string `json:"password"`
	Username string `json:"username"`
}
