#!/usr/bin/env python3
import requests, re, sys, random, datetime, zipfile
from checklib import *
from pathlib import Path

BASE_DIR = Path(__file__).absolute().resolve().parent

locations = [
    "SA", "A", "SEA", "NA", "EE", "ME"
]

class CheckMachine:
    @property

    def url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def register(self, first_name, last_name, dob):
        sess = get_initialized_session()
        sess.headers.update({'User-Agent': 'MERCOS v3.0'})
        resp = sess.post(f'{self.url}/registration.php', data={"first_name": first_name,"last_name": last_name,"dob": dob,"registration":""})
        check_response(resp, "Couldn't get register page")

        return sess

    def login(self, token):
        sess = get_initialized_session()

        sess.headers.update({'User-Agent': f'MERCOS v3.0:{token}'})
        resp = sess.get(f'{self.url}/profile.php')
        resp = sess.get(f'{self.url}/profile.php')
        check_response(resp, 'Could not get profile page at login')

        if re.findall(token, resp.text):
            return sess
        else:
            cquit(Status.MUMBLE, "Couldn't get profile page")

    def security(self, sess):
        resp = sess.get(f'{self.url}/security.php')
        check_response(resp, "Couldn't get security page")

        if re.findall(r'Your account access token is \<strong\>',resp.text):
            return(resp.text.split('Your account access token is <strong>')[1].split('</strong>')[0])
        else:
            cquit(Status.MUMBLE, "Couldn't get a Token")

    def messenger(self, sess):
        resp = sess.get(f'{self.url}/messenger.php')
        if re.findall(r'<option value="', resp.text):
            receiver = resp.text.split('<option value="')[1].split('">')[0].strip()
        else:
            cquit(Status.CORRUPT, "Couldn't get someone to send message to")

        theme = f'Ping {receiver.split(":")[0]}'
        contents = f"{rnd_string(16)}"
        sess.post(f'{self.url}/messenger.php', data={"theme": theme, "contents": contents, "receiver": receiver, "message": ""})
        resp = sess.get(f'{self.url}/messenger.php')
        check_response(resp, "Can't send message")

        if re.findall(r'{}'.format(contents),resp.text):
            return 'ok'
        else:
            cquit(Status.MUMBLE, "Couldn't send message")

    def request_merc(self,sess,commentary):
        resp = sess.get(f'{self.url}/browser.php?page=1')

        if re.findall(r'Page 1/', resp.text):
            pages = resp.text.split('Page 1/')[1].split('</span>')[0].strip()
        else:
            cquit(Status.CORRUPT, "Couldn't get pagination")

        page = random.randint(1,int(pages))

        resp = sess.get(f'{self.url}/browser.php?page={page}')
        if re.findall(r'<button type="submit" formaction="merc.php" name="alias" value="', resp.text):
            alias = resp.text.split('<button type="submit" formaction="merc.php" name="alias" value="')[1].split('"')[0]
        else:
            cquit(Status.CORRUPT, "Couldn't get commandos browser")

        payment = random.randint(1000,20000)
        location = random.randint(0,5)

        resp = sess.post(f'{self.url}/merc.php?alias={alias}', data={'alias': alias, 'location':locations[location],'theme':f'Hiring {alias}','payment':payment,'commentary':commentary,'request':''})
        check_response(resp, "Can't hire a merc")

        resp = sess.get(f'{self.url}/cabinet.php')
        if re.findall(r'{}'.format(commentary),resp.text):
            return 'ok'
        else:
            return 'corrupt'

    def request_check(self,sess,commentary):

        resp = sess.get(f'{self.url}/messenger.php')
        if re.findall(r'{}'.format(commentary),resp.text):
            return 'ok'
        else:
            return 'corrupt'
        
    def application(self, flag, name):
        open(BASE_DIR / f'utility/{name}', 'w').write(flag)
        zipfile.ZipFile(BASE_DIR / f'utility/{name}.zip', 'w').write(BASE_DIR / f'utility/{name}', arcname = name)


    def application_check(self, sess, name, flag):

        resp = sess.get(f'{self.url}/advert.php')
        check_response(resp, "Can't get application response")

        if re.findall(r'<button type="submit" formaction="applications/', resp.text):
            cvid = resp.text.split('<button type="submit" formaction="applications/')[1].split('"')[0]
        else:
            cquit(Status.MUMBLE, "Can't find CV link")

        resp = sess.get(f'{self.url}/applications/{cvid}')
        check_response(resp, "Can't get CV")

        open(BASE_DIR / f'utility/response_{name}.zip','wb').write(resp.content)
        output = zipfile.ZipFile(BASE_DIR / f'utility/response_{name}.zip').open(name).readlines()[0].strip().decode('utf-8')

        if output == flag:
            return 'ok'
        else:
            return 'corrupt'

    def advert(self, sess , name, flag):

        self.application(flag, name)
        values = {
                'application':''
                 }
        files = {
                'CV': (f'{name}.zip', open(BASE_DIR / f'utility/{name}.zip','rb'), 'application/zip')
                }

        resp = sess.post(f'{self.url}/advert.php', data=values, files=files)
        check_response(resp, "Can't apply as merc")
        
        return self.application_check(sess, name, flag)

def check(host,port):

    chk = CheckMachine(host,port)

    first_name = rnd_username()
    last_name = rnd_username()
    dob = datetime.date(1980,10,15) + datetime.timedelta(random.randint(1,3650))

    sess = chk.register(first_name,last_name,dob)
    token = chk.security(sess)

    sess = chk.login(token)
    chk.messenger(sess)

    #chk.advert(sess)
    #chk.chat(sess,merc_id,name)
    pdata = f"{first_name}{last_name}{dob}"

    cquit(Status.OK, "OK", f'{pdata}:{token}')

def put1(host,port,flag):

    chk = CheckMachine(host,port)

    first_name = rnd_username()
    last_name = rnd_username()
    dob = datetime.date(1980,10,15) + datetime.timedelta(random.randint(1,3650))

    sess = chk.register(first_name,last_name,dob)
    token = chk.security(sess)

    sess = chk.login(token)

    result = chk.request_merc(sess,flag)

    pdata = f"{first_name}{last_name}{dob}"

    if result == 'ok':
        cquit(Status.OK, f"{pdata}",f'{pdata}:{token}')
    else:
        cquit(Status.CORRUPT, 'Couldn\'t make an offer')

def get1(host,port,flag,flag_id):

    chk = CheckMachine(host,port)

    pdata,token = flag_id.strip().split(':')

    sess = chk.login(token)

    result = chk.request_check(sess,flag)

    if result == 'ok':
        cquit(Status.OK, "OK")
    else:
        cquit(Status.CORRUPT, 'Couldn\'t get request message')

def put2(host,port,flag):

    chk = CheckMachine(host,port)

    first_name = rnd_username()
    last_name = rnd_username()
    dob = datetime.date(1980,10,15) + datetime.timedelta(random.randint(1,3650))

    sess = chk.register(first_name,last_name,dob)
    token = chk.security(sess)

    sess = chk.login(token)

    result = chk.advert(sess, first_name, flag)

    pdata = f"{first_name}-{last_name}-{dob}"

    if result == 'ok':
        cquit(Status.OK, f"{pdata}",f'{pdata}:{token}')
    else:
        cquit(Status.CORRUPT, 'Couldn\'t send application')

def get2(host,port,flag,flag_id):

    chk = CheckMachine(host,port)

    pdata,token = flag_id.strip().split(':')

    sess = chk.login(token)
    name = pdata.split('-')[0]

    result = chk.application_check(sess, name, flag)

    if result == 'ok':
        cquit(Status.OK, "OK")
    else:
        cquit(Status.CORRUPT, 'Couldn\'t get application back')

if __name__ == '__main__':

    action, *args = sys.argv[1:]

    port = '6666'

    try:
        if action == 'check':

            host, = args
            check(host, port)

        elif action == 'put':
    
            host, flag_id, flag, vuln_number = args

            if vuln_number == '1':
                put1(host, port, flag)
            else:
                put2(host, port, flag)

        elif action == 'get':
            
            host, flag_id, flag, vuln_number = args

            if vuln_number == '1':
                get1(host, port, flag, flag_id)
            else:
                get2(host, port, flag, flag_id)

        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))
