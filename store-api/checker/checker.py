"""
Checker for service 'store-api'
"""
import json
import requests
import string
import random
from typing import NamedTuple, Dict
from enum import Enum

PORT = 8000


class Status(Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    ERROR = 110

    def __bool__(self):
        return self.value == Status.OK


class CheckerResult(NamedTuple):
    """
    Класс описывет результат работы чекера для push и pull
    """
    status: int
    private_info: str
    public_info: str


class PushArgs(NamedTuple):
    """
    Класс описывет аргументы для функции push
    """
    host: str  # хост на котором расположен сервис
    round_number: int  # номер текущего раунда
    flag: str  # флаг который нужно положить в сервис


class PullArgs(NamedTuple):
    """
    Класс описывет аргументы для функции pull
    """
    host: str  # хост на котором расположен сервис
    private_info: str  # приватные данные которые чекер вернул когда клал флаг
    flag: str  # Флаг который нужно получить из сервиса


class ServiceResponse(NamedTuple):
    status: int
    data: dict


def push(args: PushArgs) -> CheckerResult:
    # Check connection
    try:
        requests.post(f'http://{args.host}:{PORT}/api/checker/is-available/')
    except Exception as e:
        return CheckerResult(
            status=Status.DOWN.value,
            private_info=str(e),
            public_info=f'PUSH {Status.DOWN.value} connection error on host {args.host}'
        )

    # Check registration
    registration_data = _generate_registration_data()

    try:
        response = requests.post(
            f'http://{args.host}:{PORT}/api/v1/registration/',
            json=registration_data
        )
        try:
            data = json.loads(response.text)
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'JSON validation error on url: {response.url}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
        access_token = data.get('access_token')
        client_id = data.get('client_id')
        if access_token is None or client_id is None:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'PUSH {Status.MUMBLE.value} registration failed on {response.url}',
                public_info=f'PUSH {Status.MUMBLE.value} registration failed on url {response.url}'
                            f': access_token or client_id is undefined'
            )
        auth_header = {'Authorization': f'Bearer {access_token}'}

    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'PUSH {Status.MUMBLE.value} registration failed on host {args.host}',
            public_info=f'PUSH {Status.MUMBLE.value} registration failed on host {args.host}, error: {str(e)}'
        )

    # Check products list
    try:
        response = requests.get(
            f'http://{args.host}:{PORT}/api/v1/products/',
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'PUSH {Status.MUMBLE.value} failed to get products list on url {response.url}',
                public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on url {response.url}'
            )
        try:
            products = json.loads(response.text)
            if len(products) == 0:
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'PUSH {Status.CORRUPT.value} empty products list on url {response.url}',
                    public_info=f'PUSH {Status.CORRUPT.value} empty products list on url {response.url}'
                )
            for product in products:
                if product.get('price') not in range(3000, 100_001):
                    ...
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'JSON validation error on url: {response.url}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}'
        )

    # Check promocodes list
    try:
        response = requests.get(
            f'http://{args.host}:{PORT}/api/v1/promocodes/',
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'PUSH {Status.MUMBLE.value} failed to get promocodes list on url {response.url}',
                public_info=f'PUSH {Status.MUMBLE.value} failed to get promocodes list on url {response.url}'
            )
        try:
            promocodes = json.loads(response.text)
            if len(promocodes) == 0:
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'PUSH {Status.CORRUPT.value} empty promocodes list on url {response.url}',
                    public_info=f'PUSH {Status.CORRUPT.value} empty promocodes list on url {response.url}'
                )
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'JSON validation error on url: {response.url}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}, error: {str(e)}'
        )

    # Check client info
    try:
        response = requests.get(
            f'http://{args.host}:{PORT}/api/v1/clients/?id={client_id}',
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'PUSH {Status.MUMBLE.value} failed to get client info on url {response.url}',
                public_info=f'PUSH {Status.MUMBLE.value} failed to get client info on url {response.url}'
            )
        try:
            client_info = json.loads(response.text)
            if client_info.get('id') is None or \
                    client_info.get('email') is None or \
                    client_info.get('password') is None or \
                    client_info.get('balance') is None or \
                    client_info.get('status') is None:
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'PUSH {Status.CORRUPT.value} incomplete client info on url {response.url}',
                    public_info=f'PUSH {Status.CORRUPT.value} incomplete client info on url {response.url}'
                )
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'JSON validation error on url: {response.url}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}, error: {str(e)}'
        )

    try:
        response = requests.post(
            f'http://{args.host}:{PORT}/api/checker/put/',
            json={
                'round_number': args.round_number,
                'flag': args.flag
            }
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.CORRUPT.value,
                private_info=f'PUSH {Status.CORRUPT.value} failed to put flag on host {args.host}',
                public_info=f'PUSH {Status.CORRUPT.value} failed to put flag on host {args.host}'
            )
        return CheckerResult(
            status=Status.OK.value,
            private_info='',
            public_info='PUSH works'
        )

    except Exception as e:
        return CheckerResult(
            status=Status.CORRUPT.value,
            private_info=f'PUSH {Status.CORRUPT.value} failed to put flag on host {args.host}',
            public_info=f'PUSH {Status.CORRUPT.value} failed to put flag on host {args.host}, error: {str(e)}'
        )


def pull(args: PullArgs) -> CheckerResult:
    try:
        response = requests.get(
            f'http://{args.host}:{PORT}/api/checker/pull/?private_info={args.private_info}&flag={args.flag}',
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'PULL {Status.MUMBLE.value} can not get flag: {response.url}, content: {response.text}'
            )
        data = json.loads(response.text)
        if data.get('flag') != args.flag:
            return CheckerResult(
                status=Status.CORRUPT.value,
                private_info=str(args.private_info),
                public_info=f'PULL {Status.CORRUPT.value} Flags do not match: {response.url}, content: {response.text}'
            )
        return CheckerResult(
            status=Status.OK.value,
            private_info=str(args.private_info),
            public_info='PULL works'
        )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=str(e),
            public_info=f'PULL {Status.MUMBLE.value} flags dont match at host {args.host}, content: {e}'
        )


def _generate_registration_data() -> Dict[str, str]:
    return {
        'email': _generate_random_email(),
        'password': _generate_random_password()
    }


def _generate_random_email() -> str:
    email = 'checker_'
    for _ in range(36):
        email += random.choice(string.ascii_letters)
    email += '@checker.com'
    return email


def _generate_random_password() -> str:
    password = ''
    for _ in range(10):
        password += random.choice(string.printable)
    return password


if __name__ == '__main__':
    import sys
    action, *args = sys.argv[1:]
    result = None
    try:
        if action == 'push':
            host, round_number, flag = args
            push_args = PushArgs(host=host,round_number=round_number, flag=flag)
            # push_args.host, push_args.round_number, push_args.flag = args
            result = push(push_args)
        elif action =='pull':
            host, private_info, flag = args
            pull_args = PullArgs(host=host,private_info=private_info, flag=flag)
            result = pull(pull_args)
        else:
            result = CheckerResult(status=Status.ERROR.value, private_info='', public_info='No action found in args')
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        result = CheckerResult(status=Status.DOWN.value, private_info='', public_info='Service is DOWN')
    except SystemError as e:
        raise
    except Exception as e:
        result = CheckerResult(status=Status.ERROR.value, private_info='', public_info=e)
    if result.status != Status.OK.value:
        print(result.public_info, file=sys.stderr)
    print(result.private_info)
    exit(result.status)
