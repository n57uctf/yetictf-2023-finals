#!/usr/bin/env python3
import requests, re, sys, random, datetime, zipfile
from checklib import get_initialized_session, Status, rnd_username, rnd_string
from pathlib import Path
import secrets
from typing import NamedTuple
import json
import io
import os

locations = [
    "SA", "A", "SEA", "NA", "EE", "ME"
]

class StatusException(Exception):
    def __init__(self, status: int, private_info: str, public_info: str):
        self.status = status
        self.private_info = private_info
        self.public_info = public_info
        self.message = f"Check failed: {public_info}"


def check_status_code(resp: requests.Response, public_info: str) -> None:
    if resp.status_code >= 500:
        raise StatusException(status=sStatus.DOWN.value, private_info="", public_info=public_info)
    if not resp.ok:
        raise StatusException(status=Status.MUMBLE.value, private_info="", public_info=public_info)


class CheckMachine:
    @property

    def url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, host: str):
        self.host = host
        self.port = 6666

    def register(self, first_name: str, last_name: str, dob: datetime.date) -> requests.Session:
        sess = get_initialized_session()
        sess.headers.update({'User-Agent': 'MERCOS v3.0'})
        resp = sess.post(f'{self.url}/registration.php', data={"first_name": first_name,"last_name": last_name,"dob": dob,"registration":""})
        check_status_code(resp,"Couldn't get register page")
        return sess

    def login(self, token: str) -> requests.Session:
        sess = get_initialized_session()

        sess.headers.update({'User-Agent': f'MERCOS v3.0:{token}'})
        resp = sess.get(f'{self.url}/profile.php')
        resp = sess.get(f'{self.url}/profile.php')
        check_status_code(resp, "Could not get profile page at login")

        if re.findall(token, resp.text):
            return sess
        else:
            raise StatusException(status=Status.MUMBLE.value, private_info=token, public_info="Couldn't get profile page")

    def security(self, sess: requests.Session) -> str:
        resp = sess.get(f'{self.url}/security.php')
        check_status_code(resp, "Couldn't get security page")

        if re.findall(r'Your account access token is \<strong\>',resp.text):
            return(resp.text.split('Your account access token is <strong>')[1].split('</strong>')[0])
        else:
            raise StatusException(status=Status.MUMBLE.value, private_info=sess.headers.get("User-Agent"), public_info="Couldn't get a Token")

    def messenger(self, sess: requests.Session) -> str:
        resp = sess.get(f'{self.url}/messenger.php')
        if re.findall(r'<option value="', resp.text):
            receiver = resp.text.split('<option value="')[1].split('">')[0].strip()
        else:
            raise StatusException(status=Status.CORRUPT.value, private_info=sess.headers.get("User-Agent"), public_info="Couldn't get someone to send message to")

        theme = f'Ping {receiver.split(":")[0]}'
        contents = f"{rnd_string(16)}"
        sess.post(f'{self.url}/messenger.php', data={"theme": theme, "contents": contents, "receiver": receiver, "message": ""})
        resp = sess.get(f'{self.url}/messenger.php')
        check_status_code(resp, "Can't send message")

        if re.findall(r'{}'.format(contents),resp.text):
            return 'ok'
        else:
            raise StatusException(status=Status.MUMBLE.value, private_info=sess.headers.get("User-Agent"), public_info="Couldn't send message")

    def request_merc(self,sess: requests.Session,commentary: str) -> str:
        resp = sess.get(f'{self.url}/browser.php?page=1')

        if re.findall(r'Page 1/', resp.text):
            pages = resp.text.split('Page 1/')[1].split('</span>')[0].strip()
        else:
            raise StatusException(status=Status.CORRUPT.value, private_info=sess.headers.get("User-Agent"), public_info="Couldn't get pagination")

        page = random.randint(1,int(pages))

        resp = sess.get(f'{self.url}/browser.php?page={page}')
        if re.findall(r'<button type="submit" formaction="merc.php" name="alias" value="', resp.text):
            alias = resp.text.split('<button type="submit" formaction="merc.php" name="alias" value="')[1].split('"')[0]
        else:
            raise StatusException(status=Status.CORRUPT.value, private_info=sess.headers.get("User-Agent"), public_info="Couldn't get commandos browser")

        payment = random.randint(1000,20000)
        location = random.randint(0,5)

        resp = sess.post(f'{self.url}/merc.php?alias={alias}', data={'alias': alias, 'location':locations[location],'theme':f'Hiring {alias}','payment':payment,'commentary':commentary,'request':''})
        check_status_code(resp, "Can't hire a merc")

        resp = sess.get(f'{self.url}/cabinet.php')
        if re.findall(r'{}'.format(commentary),resp.text):
            return 'ok'
        else:
            return 'corrupt'

    def request_check(self,sess: requests.Session ,commentary: str) -> str:

        resp = sess.get(f'{self.url}/messenger.php')
        if re.findall(r'{}'.format(commentary),resp.text):
            return 'ok'
        else:
            return 'corrupt'
        
    def application(self, flag: str, name: str) -> io.BytesIO:
        zip_buffer = io.BytesIO()
        flag_bytes = io.BytesIO(flag.encode())
        with zipfile.ZipFile(zip_buffer,'w') as zip_file:
            zip_file.writestr(name, flag_bytes.getvalue())
        return zip_buffer

    def application_check(self, sess: requests.Session, name: str, flag: str) -> str:

        resp = sess.get(f'{self.url}/advert.php')
        check_status_code(resp, "Can't get application response")

        if re.findall(r'<button type="submit" formaction="applications/', resp.text):
            cvid = resp.text.split('<button type="submit" formaction="applications/')[1].split('"')[0]
        else:
            raise StatusException(status=Status.MUMBLE.value, private_info=sess.headers.get("User-Agent"), public_info="Can't find CV link")

        resp = sess.get(f'{self.url}/applications/{cvid}')
        check_status_code(resp, "Can't get CV")
        buf = io.BytesIO(resp.content)
        with zipfile.ZipFile(buf, 'r') as zipf:
            with zipf.open(name) as flagfile:
                output = flagfile.readlines()[0].strip().decode('utf-8')
        if output == flag:
            return 'ok'
        else:
            return 'corrupt'

    def advert(self, sess:requests.Session , name: str, flag: str) -> str:
        buf = self.application(flag, name)
        buf.seek(0)
        values = {
                'application':''
                 }
        files = {
                'CV': (f'{name}.zip', buf.getvalue(), 'application/zip')
                }
        resp = sess.post(f'{self.url}/advert.php', data=values, files=files)
        check_status_code(resp, "Can't apply as merc")
        return self.application_check(sess, name, flag)

class CheckerResult(NamedTuple):
    status: int
    private_info: str
    public_info: str


class PushArgs(NamedTuple):
    host: str  # хост на котором расположен сервис
    round_number: int  # номер текущего раунда
    flag: str  # флаг который нужно положить в сервис


class PullArgs(NamedTuple):
    host: str  # хост на котором расположен сервис
    private_info: str  # приватные данные которые чекер вернул когда клал флаг
    flag: str  # Флаг который нужно получить из сервиса


def push(args: PushArgs) -> CheckerResult:
    N = 2
    # FOR TESTS CHECK ENVIRON
    place = os.environ.get('PUSH_PLACE',secrets.choice(range(0,N)))
    chk = CheckMachine(args.host)
    first_name = rnd_username()
    last_name = rnd_username()
    dob = datetime.date(1980,10,15) + datetime.timedelta(random.randint(1,3650))
    try:  
        sess = chk.register(first_name,last_name,dob)
        token = chk.security(sess)
        sess = chk.login(token)
        if place == 0:
            result = chk.request_merc(sess, args.flag)
        else:
            result = chk.advert(sess, first_name, args.flag)
        pdata = f"{first_name}-{last_name}-{dob}"

        if result == 'ok':
            return CheckerResult(status=Status.OK.value, private_info=f"{place}:{pdata}:{token}", public_info=f"{pdata}")
        else:
            raise StatusException(status=Status.CORRUPT.value, private_info=f"{place}:{pdata}:{token}", public_info="Couldn't make an offer")
    except StatusException as se:
        return CheckerResult(status=se.status, private_info=se.private_info, public_info=se.public_info)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    except SystemError as e:
        raise
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value, private_info=str(e), public_info="Checker Error")

def pull(args: PullArgs) -> CheckerResult:

    chk = CheckMachine(args.host)

    place, pdata, token = args.private_info.strip().split(':')
    try:
        sess = chk.login(token)
        if place == 0:  
            result = chk.request_check(sess,args.flag)

            if result == 'ok':
                return CheckerResult(status=Status.OK.value, private_info=f"{place}:{pdata}:{token}", public_info="PULL OK")
            else:
                return CheckerResult(status=Status.CORRUPT.value, private_info=f"{place}:{pdata}:{token}", public_info="Couldn't get request message")
        else: 
            name = pdata.split('-')[0]

            result = chk.application_check(sess, name, args.flag)

            if result == 'ok':
                return CheckerResult(status=Status.OK.value, private_info=f"{place}:{pdata}:{token}", public_info="PULL OK")
            else:
                return CheckerResult(status=Status.CORRUPT.value, private_info=f"{place}:{pdata}:{token}", public_info="Couldn't get application back")
    except StatusException as se:
        return CheckerResult(status=se.status, private_info=se.private_info, public_info=se.public_info)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    except SystemError as e:
        raise
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value, private_info=str(e), public_info="Checker Error")
