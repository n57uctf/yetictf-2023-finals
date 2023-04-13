"""
Checker for service 'store-api'
"""
from __future__ import annotations
import json
import requests
import string
import random
import hashlib
import base64
from typing import NamedTuple, Dict, Tuple
from enum import Enum

PORT = 8080


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


def push(args: PushArgs) -> CheckerResult:
    api_base_url = f'http://{args.host}:{PORT}/api/v1'

    # Check registration
    registration_data = _generate_registration_data()
    try:
        response = requests.post(
            f'{api_base_url}/registration/',
            json=registration_data
        )
        if response.status_code != 201:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.MUMBLE.value} can not register on {response.url}'
            )
        try:
            data = json.loads(response.text)
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
        email = data.get('email')
        password = data.get('password')
        client_id = data.get('id')
        balance = data.get('balance')
        if email is None or password is None or client_id is None or balance is None:
            return CheckerResult(
                status=Status.CORRUPT.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.CORRUPT.value} incomplete registration response on {response.url}'
                            f': email, password, balance or id is undefined'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} registration failed on host {args.host}, error: {str(e)}'
        )

    # Check authorization
    try:
        response = requests.post(
            f'{api_base_url}/auth/',
            json=registration_data
        )
        try:
            data = json.loads(response.text)
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        if access_token is None or refresh_token is None:
            return CheckerResult(
                status=Status.CORRUPT.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.CORRUPT.value} incomplete authorization response on {response.url}'
                            f': email, password, balance or id is undefined'
            )
        auth_header = {'Authorization': f'Bearer {access_token}'}
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} authorization failed on host {args.host}, error: {str(e)}'
        )

    # Check products list
    try:
        response = requests.get(
            f'{api_base_url}/products/',
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
            test_product = products[0]
            for product in products:
                if product.get('price') not in range(3000, 1_000_001):
                    return CheckerResult(
                        status=Status.CORRUPT.value,
                        private_info=f'{response.status_code}',
                        public_info=f'PUSH {Status.CORRUPT.value} invalid product price on url {response.url}'
                    )
        except Exception as e:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{str(e)}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}'
        )

    # Check promocodes list
    try:
        response = requests.get(
            f'{api_base_url}/promocodes/',
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.MUMBLE.value} failed to get promocodes list on url {response.url}'
            )
        try:
            promocodes = json.loads(response.text)
            if len(promocodes) == 0:
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PUSH {Status.CORRUPT.value} empty promocodes list on url {response.url}'
                )
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}, error: {str(e)}'
        )

    # Check client info
    try:
        response = requests.get(
            f'{api_base_url}/clients/?id={client_id}',
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
                    client_info.get('balance') is None or \
                    client_info.get('password') is None:
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PUSH {Status.CORRUPT.value} incomplete client info on url {response.url}'
                )
        except Exception as e:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{str(e)}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}, error: {str(e)}'
        )

    # Check adding product to basket
    try:
        response = requests.post(
            f'{api_base_url}/basket/add/',
            json={
                'client_id': client_id,
                'product_id': test_product.get('id')
            },
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.MUMBLE.value} failed to add product to basket on url {response.url}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}, error: {str(e)}'
        )

    # Check creating order
    try:
        response = requests.post(
            f'{api_base_url}/orders/create/',
            json={
                'client_id': client_id,
            },
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.MUMBLE.value} failed to create order on url {response.url}'
            )
        try:
            order_data = json.loads(response.text)
            order_id = order_data.get('order_id')
            if order_id is None or not str(order_id).isdigit():
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PUSH {Status.CORRUPT.value} incomplete response on url {response.url}'
                )
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.MUMBLE.value} failed to get products list on host {args.host}, error: {str(e)}'
        )

    # Insert flag
    try:
        name, description, price = _get_random_product_info(args.flag)
        response = requests.post(
            f'{api_base_url}/products/add/',
            json={
                'round_number': args.round_number,
                'name': name,
                'description': description,
                'price': price
            },
            headers=auth_header
        )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.CORRUPT.value,
                private_info=f'{response.status_code}',
                public_info=f'PUSH {Status.CORRUPT.value} failed to put flag on host {args.host}'
            )
        try:
            data = json.loads(response.text)
            product_id = data.get('product_id')
            secret_key = data.get('secret_key')
            if product_id is None or secret_key is None:
                return CheckerResult(
                    status=Status.CORRUPT.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PUSH {Status.CORRUPT.value} incomplete product adding response on {response.url}'
                )
        except:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'JSON validation error on url: {response.url}, content: {response.text}'
            )
        _private_info = registration_data.copy()
        _private_info['round_number'] = args.round_number
        _private_info['access_token'] = access_token
        _private_info['refresh_token'] = refresh_token
        _private_info['product_id'] = product_id
        _private_info['secret_key'] = secret_key
        return CheckerResult(
            status=Status.OK.value,
            private_info=json.dumps(_private_info),
            public_info='PUSH works'
        )
    except Exception as e:
        return CheckerResult(
            status=Status.CORRUPT.value,
            private_info=f'{str(e)}',
            public_info=f'PUSH {Status.CORRUPT.value} failed to put flag on host {args.host}, error: {str(e)}'
        )


def pull(args: PullArgs) -> CheckerResult:
    api_base_url = f'http://{args.host}:{PORT}/api/v1'
    private_info = json.loads(args.private_info)
    email = private_info.get('email')
    password = private_info.get('password')
    round_number = private_info.get('round_number')
    access_token = private_info.get('access_token')
    refresh_token = private_info.get('refresh_token')
    product_id = private_info.get('product_id')
    secret_key = private_info.get('secret_key')
    # Check auth
    try:
        response = requests.post(
            f'{api_base_url}/auth/',
            json={
                'email': email,
                'password': password
            }
        )
        if response.status_code != 200:
            if response.status_code != 304:
                return CheckerResult(
                    status=Status.MUMBLE.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PULL {Status.MUMBLE.value} can not login {response.url} - {response.status_code}'
                )
        else:
            response_data = json.loads(response.text)
            access_token = response_data.get('access_token')
            refresh_token = response_data.get('refresh_token')
            if access_token is None or refresh_token is None:
                return CheckerResult(
                    status=Status.MUMBLE.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PULL {Status.MUMBLE.value} can not login {response.url} - {response.status_code}'
                )
            private_info['access_token'] = access_token
            private_info['refresh_token'] = refresh_token
    except Exception as e:
        return CheckerResult(
            status=Status.MUMBLE.value,
            private_info=str(e),
            public_info=f'PULL {Status.MUMBLE.value} can not get flag at host {args.host}, content: {e}'
        )
    # Get flag
    auth_header = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(
            f'{api_base_url}/products/?id={product_id}',
            headers=auth_header
        )
        if response.status_code == 403:
            new_tokens = requests.patch(f'{api_base_url}/tokens/update/', json={
                'access_token': access_token,
                'refresh_token': refresh_token
            })
            if new_tokens.status_code != 200:
                return CheckerResult(
                    status=Status.MUMBLE.value,
                    private_info=f'{response.status_code}',
                    public_info=f'PULL {Status.MUMBLE.value} can not get flag: {response.url}, content: {response.text}'
                )
            resp_data = json.loads(new_tokens.text)
            access_token = resp_data.get('access_token')
            private_info['access_token'] = access_token
            auth_header = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                f'{api_base_url}/products/?id={product_id}',
                headers=auth_header
            )
        if response.status_code != 200:
            return CheckerResult(
                status=Status.MUMBLE.value,
                private_info=f'{response.status_code}',
                public_info=f'PULL {Status.MUMBLE.value} can not get flag: {response.url}, content: {response.text}'
            )
        data = json.loads(response.text)[0]
        description = data.get('description')
        price = data.get('price')
        if price > 1_000_000:
            return CheckerResult(
                status=Status.CORRUPT.value,
                private_info=str(args.private_info),
                public_info=f'PULL {Status.CORRUPT.value} can not get flag: {response.url}, price is too high'
            )
        decoded_description = _decode_string(description, secret_key)
        decoded_description = decoded_description.split()
        if args.flag not in decoded_description:
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
            public_info=f'PULL {Status.MUMBLE.value} can not get flag at host {args.host}, content: {e}'
        )


def _generate_registration_data() -> Dict[str, str | int]:
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
    for _ in range(30):
        password += random.choice(string.printable)
    return password


def _decode_string(string_: str, secret_key: str) -> str:
    """Decodes the string using secret key
    :param string_: string to decode
    :type string_: str
    :param secret_key: key that will be used to decode the string
    :type secret_key: str
    :return: decoded string
    :rtype: str
    """
    sha256 = hashlib.sha256()
    sha256.update(secret_key.encode())
    encoded_key = sha256.digest()
    decoded_bytes = bytearray(base64.b64decode(string_))
    decoded = ''
    for i in range(len(decoded_bytes)):
        key_index = i % len(encoded_key)
        decoded += chr(decoded_bytes[i] ^ encoded_key[key_index])
    return decoded


def _get_random_product_info(flag: str) -> Tuple[str, str, int]:
    name = random.choice(list(_products.keys()))
    description = _products[name]['description']
    description_list = description.split()
    middle_index = len(description_list) // 2
    description_list.insert(middle_index, flag)
    description = ' '.join(description_list)
    price = _products[name]['price']
    return name, description, price


_products = {
    "Eco-friendly reusable water bottle": {
        "description": "Made from durable and sustainable materials, this bottle is perfect for on-the-go hydration.",
        "price": 980000
    },
    "Smartphone gimbal stabilizer": {
        "description": "Capture smooth, professional-grade video on your smartphone with this 3-axis gimbal stabilizer.",
        "price": 950000
    },
    "Wireless noise-cancelling headphones": {
        "description": "Block out distractions and immerse yourself in your music with these wireless noise-cancelling headphones.",
        "price": 990000
    },
    "Robot vacuum cleaner": {
        "description": "Keep your floors clean without lifting a finger with this robotic vacuum cleaner.",
        "price": 975000
    },
    "Instant Pot": {
        "description": "Cook meals quickly and easily with this versatile pressure cooker and multi-cooker.",
        "price": 960000
    },
    "Fitness tracker": {
        "description": "Track your daily activity, workouts, and sleep with this stylish and functional fitness tracker.",
        "price": 930000
    },
    "Cordless drill": {
        "description": "Take on DIY projects with ease using this powerful and portable cordless drill.",
        "price": 985000
    },
    "Stand mixer": {
        "description": "Whip up delicious baked goods and more with this high-quality stand mixer.",
        "price": 970000
    },
    "Eco-Friendly Reusable Water Bottle": {
        "description": "Stay hydrated while helping the environment with this reusable water bottle made from sustainable materials.",
        "price": 970000
    },
    "Noise-Cancelling Headphones": {
        "description": "Block out distracting sounds and immerse yourself in music with these noise-cancelling headphones.",
        "price": 920000
    },
    "Smartphone Car Mount": {
        "description": "Securely mount your phone to your car dashboard for safe and easy navigation while driving.",
        "price": 980000
    },
    "Fitness Tracker": {
        "description": "Track your daily activity, sleep, and heart rate with this sleek and stylish fitness tracker.",
        "price": 940000
    },
    "Non-Stick Cooking Set": {
        "description": "Cook like a pro with this durable and easy-to-clean non-stick cooking set that includes pots and pans of various sizes.",
        "price": 990000
    },
    "Portable Power Bank": {
        "description": "Charge your phone or tablet on the go with this compact and high-capacity power bank that fits in your pocket.",
        "price": 960000
    },
    "Home Security Camera": {
        "description": "Keep an eye on your home and loved ones with this high-definition security camera that sends alerts to your phone.",
        "price": 940000
    },
    "Smart Doorbell": {
        "description": "A doorbell with a camera that sends notifications to your phone and allows you to see and speak to visitors",
        "price": 950000
    },
    "Portable Air Conditioner": {
        "description": "A compact air conditioner that can easily be moved from room to room",
        "price": 920000
    },
    "Smart Plant Pot": {
        "description": "A plant pot that monitors soil moisture and fertilization levels and sends alerts to your phone",
        "price": 940000
    },
    "Electric Kettle": {
        "description": "A fast-boiling kettle with a temperature control function and automatic shutoff",
        "price": 900000
    },
    "Robot Vacuum": {
        "description": "A self-navigating vacuum that can be controlled with a smartphone app",
        "price": 980000
    }
}

if __name__ == '__main__':
    import sys

    action, *args = sys.argv[1:]
    result = None
    try:
        if action == 'push':
            host, round_number, flag = args
            push_args = PushArgs(host=host, round_number=round_number, flag=flag)
            result = push(push_args)
        elif action == 'pull':
            host, private_info, flag = args
            pull_args = PullArgs(host=host, private_info=private_info, flag=flag)
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
