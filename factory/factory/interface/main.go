package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

var jwtKey = []byte("my_secret_key")
var db DB
var mb Modbus

func main() {
	var err error
	log.Println("Creating db...")
	db, err = CreateDB("./db.sqlite")
	defer db.Close()
	if err != nil {
		log.Printf("Failed to init db: %v\n", err)
		return
	}
	log.Printf("Checking plc on addr %v\n", os.Getenv("plc_addr"))
	if ok, err := TestModbus(os.Getenv("plc_addr"), true); ok && err == nil {
		log.Println("PLC healthy")
	} else {
		log.Println("PLC unhealthy")
	}

	mb, _ = CreateModbus(os.Getenv("plc_addr"))
	router := mux.NewRouter()
	router.HandleFunc("/health", healthHandler).Methods("GET")
	router.HandleFunc("/signin", signinHandler).Methods("POST")
	router.HandleFunc("/signup", signupHandler).Methods("POST")
	router.HandleFunc("/refresh", refreshHandler).Methods("POST")
	router.HandleFunc("/logout", logoutHandler).Methods("POST")
	router.HandleFunc("/http2mod", http2modHandler).Methods("POST")
	router.HandleFunc("/control", controlHandler).Methods("POST")
	router.HandleFunc("/history", historyHandler).Methods("GET")
	router.HandleFunc("/temp", tempHandler).Methods("GET")

	mb.SetData("00aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

	router.Use(PanicRecoveryMiddleware, LoggingMiddleware, TokenMiddleware)

	server := &http.Server{
		Handler: router,
		Addr:    os.Getenv("interface_addr"),
	}
	log.Printf("Server is listening on addr %v...\n", os.Getenv("interface_addr"))
	server.ListenAndServe()
}
