from typing import NamedTuple  # Делаем обязательный импорт
import enum
import requests
import random
import string
import json

class Status(enum.Enum):
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
    host: str # хост на котором расположен сервис
    round_number: int  # номер текущего раунда
    flag: str  # флаг который нужно положить в сервис


class PullArgs(NamedTuple):
    """
    Класс описывет аргументы для функции pull
    """
    host: str # хост на котором расположен сервис
    private_info: str  # приватные данные которые чекер вернул когда клал флаг
    flag: str  # Флаг который нужно получить из сервиса

PORT = 7777
passwords = ( 'qwertyui')
names = ('Aaberg', 'Abbot', 'Abernon', 'Abram', 'Ackerley', 'Adalbert', 'Adamsen', 'Ade', 'Ader', 'Adlare', 'Adore', 'Adrienne', 'Afton', 'Agle', 'Ahab', 'Aida', 'Ailyn', 'Ajay', 'Alabaster', 'Alarise', 'Albertine', 'Alcott', 'Aldric', 'Alejoa', 'Alexandr', 'Alfons', 'Alice', 'Alisia', 'Allare', 'Allina', 'Allys', 'Aloise', 'Alrich', 'Alva', 'Alwin', 'Amadas', 'Amand', 'Amasa', 'Ambrosia', 'Amethist', 'Ammann', 'Ana', 'Anastice', 'Anderegg', 'Andres', 'Anet', 'Angelita', 'Anissa', 'Annabelle', 'Annie', 'Anselmo', 'Antone', 'Anzovin', 'Aprilette', 'Arbe', 'Ardehs', 'Ardrey', 'Argyle', 'Arielle', 'Arleyne', 'Armando', 'Arnelle', 'Arratoon', 'Artima', 'Arvonio', 'Asher', 'Ashraf', 'Astraea', 'Athal', 'Atrice', 'Auberon', 'Audra', 'Augusta', 'Aurelius', 'Autry', 'Avictor', 'Axe', 'Aziza', 'Bachman', 'Baiel', 'Bakki', 'Ballard', 'Bander', 'Bar', 'Barbi', 'Barimah', 'Barnie', 'Barry', 'Bartley', 'Bashuk', 'Batha', 'Baudoin', 'Bayly', 'Beasley', 'Beberg', 'Beeck', 'Behrens', 'Belayneh', 'Belle', 'Bendicta', 'Benil', 'Bennink', 'Berardo', 'Bergmann', 'Berlauda', 'Bernelle', 'Berry', 'Bertolde', 'Bethel', 'Betty', 'Bevis', 'Bible', 'Bigod', 'Bilow', 'Birdie', 'Bixby', 'Blakelee', 'Blaseio', 'Blithe', 'Bluhm', 'Bobbette', 'Boehmer', 'Bohman', 'Bollen', 'Bonina', 'Booker', 'Borden', 'Borreri', 'Boucher', 'Bowden', 'Boycie', 'Brackett', 'Braeunig', 'Brandie', 'Braunstein', 'Breen', 'Brenna', 'Briana', 'Brietta', 'Bringhurst', 'Brittany', 'Broder', 'Bronnie', 'Brott', 'Brunella', 'Bryner', 'Buckley', 'Buffy', 'Bum', 'Burchett', 'Burkley', 'Burny', 'Busby', 'Butte', 'Byrom', 'Cadmarr', 'Caitrin', 'Calia', 'Calloway', 'Camel', 'Campbell', 'Candyce', 'Caplan', 'Carbone', 'Cargian', 'Carlen', 'Carlstrom', 'Carmencita', 'Carolina', 'Carrick', 'Cary', 'Casimire', 'Cassondra', 'Catha', 'Catima', 'Cavanagh', 'Ceciley', 'Celestyn', 'Centonze', 'Chace', 'Chak', 'Chandless', 'Chapman', 'Charla', 'Charmion', 'Chavaree', 'Chema', 'Cherice', 'Chesney', 'Chickie', 'Chiou', 'Chon', 'Christalle', 'Christis', 'Chu', 'Ciapha', 'Cinda', 'Cirone', 'Clarabelle', 'Clarisse', 'Claudio', 'Clein', 'Cleodal', 'Cliff', 'Close', 'Cnut', 'Codee', 'Cohe', 'Colburn', 'Collen', 'Colpin', 'Combe', 'Conchita', 'Conner', 'Constant', 'Cooley', 'Corabelle', 'Cordie', 'Corin', 'Cornelie', 'Corrinne', 'Cosetta', 'Cottrell', 'Covell', 'Craggy', 'Crean', 'Cressler', 'Cristian', 'Crompton', 'Cruickshank', 'Culliton', 'Currey', 'Cutlip', 'Cynara', 'Cyril', 'Dael', 'Dahlstrom', 'Dallis', 'Dambro', 'Danczyk', 'Daniell', 'Dante', 'Darby', 'Darice', 'Darrelle', 'Dasha', 'Davey', 'Dawn', 'Dearborn', 'Decato', 'Deedee', 'Dela', 'Delija', 'Delos', 'Deming', 'Denie', 'Denver', 'Dermot', 'Des', 'Deste', 'Devland', 'Dewitt', 'Dianemarie', 'Dich', 'Dielle', 'Dimitri', 'Dinsmore', 'Dittman', 'Docile', 'Doi', 'Dolphin', 'Dominus', 'Donela', 'Donny', 'Dorcus', 'Dorinda', 'Dorothi', 'Dosi', 'Douglas', 'Downs', 'Dream', 'Driskill', 'Drummond', 'Dudden', 'Dulcia', 'Dunham', 'Durant', 'Durward', 'Duvall', 'Dyanne', 'Eachelle', 'Earley', 'Ebby', 'Eckart', 'Edea', 'Edina', 'Edmonds', 'Edva', 'Egarton', 'Ehrlich', 'Eisenstark', 'Elberta', 'Eldreeda', 'Eleph', 'Eliathan', 'Elish', 'Ellerd', 'Ellora', 'Elnore', 'Elsie', 'Elvis', 'Emalia', 'Emersen', 'Emmalee', 'Emmuela', 'Eng', 'Ennis', 'Ephrayim', 'Erastus', 'Erica', 'Erland', 'Ermine', 'Erroll', 'Esma', 'Estell', 'Ethan', 'Etoile', 'Eugene', 'Euphemie', 'Evander', 'Evelyn', 'Evslin', 'Ezana', 'Fabio', 'Fadil', 'Fairman', 'Fanchon', 'Fari', 'Farny', 'Fasano', 'Faus', 'Fawnia', 'Fedak', 'Feldt', 'Feliza', 'Fenner', 'Feriga', 'Ferrel', 'Fia', 'Fiertz', 'Fillander', 'Fini', 'Firman', 'Fitzpatrick', 'Fleeman', 'Flip', 'Florin', 'Flss', 'Fonsie', 'Forras', 'Foskett', 'France', 'Francoise', 'Franz', 'Freda', 'Fredette', 'French', 'Friedberg', 'Frodeen', 'Fruma', 'Fullerton', 'Fusco', 'Gabrielle', 'Gahan', 'Galatia', 'Gamali', 'Garaway', 'Gare', 'Garlen', 'Garris', 'Gaspar', 'Gauldin', 'Gavrielle', 'Gayner', 'Gefen', 'Gemina', 'Genisia', 'Geoffry', 'Georglana', 'Gerfen', 'Germana', 'Gerstner', 'Gherardi', 'Gibb', 'Giesser', 'Gilberto', 'Gill', 'Gilmore', 'Ginny', 'Girardi', 'Giuditta', 'Gladis', 'Glenda', 'Glover', 'Godber', 'Goer', 'Goldin', 'Gomar', 'Goodden', 'Gordie', 'Gotcher', 'Gow', 'Graham', 'Granny', 'Graybill', 'Greenstein', 'Gregory', 'Greyso', 'Grimbald', 'Groark', 'Grosvenor', 'Gualterio', 'Guild', 'Gunilla', 'Gusba', 'Guthrey', 'Gwenora', 'Hachmann', 'Haerle', 'Haile', 'Haldane', 'Hall', 'Halpern', 'Hamid', 'Hamrnand', 'Hankins', 'Hanser', 'Hardan', 'Harim', 'Harms', 'Harriette', 'Hartmunn', 'Hasheem', 'Hatfield', 'Havener', 'Hayman', 'Hazen', 'Hebert', 'Hedvah', 'Heidie', 'Heise', 'Helenka', 'Helsie', 'Hendry', 'Henricks', 'Hepsiba', 'Hermann', 'Herrah', 'Hertz', 'Hess', 'Hewie', 'Hidie', 'Hilary', 'Hillegass', 'Hime', 'Hiroshi', 'Hoashis', 'Hoem', 'Hola', 'Hollinger', 'Holtorf', 'Honora', 'Horacio', 'Hortense', 'Hound', 'Howlond', 'Huberman', 'Hufnagel', 'Hulen', 'Hun', 'Hurless', 'Hutchinson', 'Hyde', 'Iaria', 'Idel', 'Ieso', 'Ihab', 'Ilise', 'Imelda', 'Infeld', 'Ingold', 'Iny', 'Iphigeniah', 'Irmina', 'Isac', 'Isidora', 'Israel', 'Ive', 'Iz', 'Jacie', 'Jacoba', 'Jacquette', 'Jaffe', 'Jala', 'Jamison', 'Janelle', 'Janis', 'Janyte', 'Jariah', 'Jarvis', 'Jaye', 'Jeanna', 'Jeffcott', 'Jehovah', 'Jen', 'Jennee', 'Jerad', 'Jerol', 'Jesher', 'Jeth', 'Jillana', 'JoAnne', 'Jobe', 'Jody', 'Johanan', 'Johns', 'Jolenta', 'Jones', 'Jordon', 'Joselow', 'Josselyn', 'Jozef', 'Judus', 'Julie', 'Juni', 'Justine', 'Kaela', 'Kaitlynn', 'Kalin', 'Kama', 'Kania', 'Karas', 'Karissa', 'Karlyn', 'Kary', 'Kassity', 'Katheryn', 'Katonah', 'Kaufmann', 'Kaz', 'Keeler', 'Keiko', 'Kelila', 'Kelsy', 'Kendrah', 'Kenneth', 'Kenwee', 'Kerman', 'Kery', 'Kevin', 'Khichabia', 'Kieran', 'Killian', 'Kimmel', 'Kingston', 'Kira', 'Kirsteni', 'Kitty', 'Klement', 'Klos', 'Knowle', 'Kobylak', 'Kolk', 'Konstantine', 'Korenblat', 'Kosel', 'Kowtko', 'Krause', 'Krenn', 'Kristel', 'Krock', 'Krystalle', 'Kumler', 'Kusin', 'Kyla', 'LaMee', 'Lachman', 'Lahey', 'Lali', 'Lammond', 'Lancelot', 'Landry', 'Langston', 'Laraine', 'Larkin', 'Lashondra', 'Latimer', 'Latt', 'Launcelot', 'Lauretta', 'Lavena', 'Lawson', 'LeMay', 'Leanora', 'Leclair', 'Leesen', 'Leid', 'Lela', 'Lemon', 'Lenno', 'Leon', 'Leontina', 'Leshia', 'Letizia', 'Leveridge', 'Lewellen', 'Lezlie', 'Libby', 'Lidia', 'Lila', 'Lily', 'Lindbom', 'Lindy', 'Linnie', 'Lipscomb', 'Liss', 'Liu', 'Lizzy', 'Lodmilla', 'Lolande', 'Longan', 'Lopes', 'Lorena', 'Lorinda', 'Lorry', 'Lotus', 'Loux', 'Lowney', 'Lubeck', 'Lucic', 'Lucy', 'Luelle', 'Lulita', 'Lunneta', 'Lustick', 'Lyford', 'Lynelle', 'Lysander', 'MacGregor', 'Maccarone', 'Macy', 'Madelaine', 'Madonia', 'Magda', 'Magna', 'Mahon', 'Maire', 'Malamud', 'Malia', 'Mallis', 'Malvie', 'Mandi', 'Manny', 'Manya', 'Marcellina', 'Marcoux', 'Margalo', 'Margit', 'Mariano', 'Marigolde', 'Marion', 'Market', 'Marler', 'Maro', 'Marrissa', 'Martelli', 'Martinson', 'Marya', 'Marysa', 'Mastic', 'Mathian', 'Matthaus', 'Maud', 'Maurili', 'Maxentia', 'Mayce', 'Mazonson', 'McClelland', 'McCullough', 'McGraw', 'McKinney', 'McNeely', 'Meaghan', 'Medora', 'Meghan', 'Mela', 'Melessa', 'Mella', 'Melody', 'Mendelsohn', 'Meraree', 'Meredi', 'Merlin', 'Merrill', 'Meta', 'Micaela', 'Michelina', 'Middendorf', 'Mikael', 'Milburr', 'Millar', 'Milon', 'Miner', 'Minta', 'Mirilla', 'Mitinger', 'Modeste', 'Mohr', 'Molly', 'Monika', 'Monteith', 'Mord', 'Morganne', 'Morra', 'Mosa', 'Mossman', 'Moyna', 'Mulcahy', 'Munford', 'Murdock', 'Muslim', 'Myra', 'Naamana', 'Nadean', 'Nahshu', 'Names', 'Nanny', 'Nari', 'Natal', 'Nathanial', 'Nazar', 'Neddy', 'Neile', 'Nellir', 'Neri', 'Nessie', 'Neumark', 'Newby', 'Niall', 'Nicki', 'Nicolella', 'Nightingale', 'Nikos', 'Niobe', 'Noach', 'Noell', 'Nollie', 'Nord', 'Normi', 'Norvell', 'Nozicka', 'Nyhagen', 'Obau', 'Obrien', 'Odele', 'Odom', 'Ogg', 'Olatha', 'Olga', 'Olly', 'Olympe', 'Ondine', 'Oona', 'Orbadiah', 'Orgell', 'Orlando', 'Ornstead', 'Orthman', 'Osborn', 'Ossie', 'Othelia', 'Otto', 'Ozzie', "O'Meara", 'Packer', 'Paige', 'Palma', 'Panayiotis', 'Paola', 'Pardoes', 'Parrish', 'Pascale', 'Patience', 'Patterman', 'Paulita', 'Paxton', 'Pearlman', 'Pedroza', 'Pelaga', 'Pena', 'Pentha', 'Per', 'Perloff', 'Perseus', 'Peterson', 'Petronilla', 'Pfeifer', 'Phene', 'Philine', 'Phillis', 'Phox', 'Piefer', 'Pike', 'Pinter', 'Piselli', 'Plante', 'Plumbo', 'Polito', 'Pomona', 'Popelka', 'Portwne', 'Power', 'Prendergast', 'Priebe', 'Prissie', 'Proudfoot', 'Pryor', 'Pulcheria', 'Puto', 'Queenie', 'Quince', 'Quiteris', 'Rachel', 'Radloff', 'Raffaello', 'Rahr', 'Rakia', 'Ramey', 'Randal', 'Ranit', 'Rapp', 'Ratib', 'Ray', 'Rayshell', 'Rebbecca', 'Redfield', 'Reeva', 'Reiche', 'Reinhard', 'Rem', 'Rene', 'Renwick', 'Reuven', 'Rhea', 'Rhodie', 'Ribble', 'Richela', 'Ricker', 'Riegel', 'Riki', 'Rintoul', 'Ritchie', 'Roana', 'Robert', 'Robyn', 'Rockie', 'Rodie', 'Roer', 'Rolando', 'Romanas', 'Romonda', 'Ronny', 'Rosa', 'Rosanne', 'Rosemare', 'Rosenthal', 'Rossen', 'Rothwell', 'Rowney', 'Roz', 'Ruberta', 'Rudin', 'Rufford', 'Ruperta', 'Russo', 'Ruthy', 'Saba', 'Sachi', 'Sadler', 'Saied', 'Salas', 'Sallee', 'Salvador', 'Sami', 'Sanborne', 'Sandry', 'Santa', 'Sarajane', 'Sartin', 'Saum', 'Savior', 'Saylor', 'Schaeffer', 'Scheider', 'Schlesinger', 'Schoening', 'Schriever', 'Schwartz', 'Scotti', 'Seaden', 'Sebastiano', 'Seem', 'Seiter', 'Selhorst', 'Selmner', 'Seow', 'Sergius', 'Seto', 'Seymour', 'Shakti', 'Shanie', 'Shargel', 'Shaughnessy', 'Shear', 'Shel', 'Shelton', 'Shere', 'Sherr', 'Sheya', 'Shippee', 'Shoifet', 'Shue', 'Shute', 'Sibley', 'Sidon', 'Siesser', 'Sik', 'Silsby', 'Simah', 'Sinclair', 'Sirotek', 'Skantze', 'Skipton', 'Slayton', 'Smart', 'So', 'Solberg', 'Sommer', 'Sophey', 'Sosna', 'Spalla', 'Spence', 'Spohr', 'Stacey', 'Stan', 'Stanton', 'Staten', 'Steele', 'Steinke', 'Stephenie', 'Stevena', 'Stillas', 'Stoecker', 'Stouffer', 'Streetman', 'Stroup', 'Stutsman', 'Sugihara', 'Sunda', 'Susana', 'Suzan', 'Swamy', 'Swetlana', 'Sybille', 'Synn', 'Tace', 'Taggart', 'Talbert', 'Tam', 'Tammie', 'Tannenbaum', 'Tarr', 'Tate', 'Tawney', 'Tedda', 'Tegan', 'Ten', 'Terbecki', 'Terrance', 'Tertia', 'Tews', 'Thanh', 'Thedrick', 'Therese', 'Thibaut', 'Thomajan', 'Thorma', 'Three', 'Tibbitts', 'Tiertza')

def get_random_username():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name
def get_random_password():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(passwords)
    password = passwords[random.randint(0, ran - 1)]
    return password + str(random.randint(10000, 99999))
def get_random_email():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + "@" + str(random.randint(10000, 99999)) + ".ru"
def get_random_name():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(100, 999))
def get_random_lastname():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(100, 999))
def get_random_patronymic():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(100, 999))

def push(args: PushArgs) -> CheckerResult:
    url = f'http://{args.host}:{PORT}/bank'
    json1={ 
        "username":get_random_username(),
        "password":get_random_password(),
        "email":get_random_email(),
        "firstName":get_random_name(),
        "lastName":get_random_lastname(),
        "patronymic":get_random_patronymic()}
    try:
        resp = requests.post(f'{url}/register', json=json1, timeout = 2)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PUSH {Status.MUMBLE.value} {resp.url} - {resp.status_code}')
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    username = get_random_username()
    password=get_random_password()
    email=get_random_email()
    firstName=get_random_name()
    lastName=get_random_lastname()
    patronymic=get_random_patronymic()
    dictionary ={ 
    "username" : username,
    "password" : password,
    "email" : email,
    "firstName" : firstName,
    "lastName" : lastName,
    "patronymic" : patronymic
    }
    json1={ 
        "username":username,
        "password":password,
        "email":email,
        "firstName":firstName,
        "lastName":lastName,
        "patronymic":patronymic}
    json_object = json.dumps(dictionary) 
    try:
        resp = requests.post(f'{url}/register', json=json1, timeout = 2)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PUSH {Status.MUMBLE.value} {resp.url} - {resp.status_code}')
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    payload = {'username':username, 'password': password}
    try:
        resp = requests.post(f'{url}/login', params = payload)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PUSH {Status.MUMBLE.value} {resp.url} - {resp.status_code}')
        token = resp.json()['accessToken']
        resp = requests.get(f'{url}/user/getAcNum', headers={'Authorization': 'Bearer ' + token}, timeout = 2)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PUSH {Status.MUMBLE.value} {resp.url} - {resp.status_code}') 
        toAcNum = resp.json()[-1]['accountNumber']
        json1={'to':toAcNum, 'amount':'1', 'comment':args.flag}
        resp = requests.post(f'{url}/user/transfer', headers={'Authorization': 'Bearer ' + token}, json=json1, timeout = 2)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PUSH {Status.MUMBLE.value} {resp.url} - {resp.status_code}')
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.ERROR.value} Can not connect')
    return CheckerResult(status=Status.OK.value, private_info=json_object, public_info='PUSH works')

def pull(args: PullArgs) -> CheckerResult:
    url = f'http://{args.host}:{PORT}/bank'
    username = json.loads(args.private_info)['username']
    password = json.loads(args.private_info)['password']
    payload = {'username':username, 'password': password}
    try:
        resp = requests.post(f'{url}/login', params = payload)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PULL {Status.MUMBLE.value} {resp.url} - {resp.status_code}')
        token = resp.json()['accessToken']
        resp = requests.get(f'{url}/user/lastTransfer', headers={'Authorization': 'Bearer ' + token}, timeout = 2)
        if resp.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PULL {Status.MUMBLE.value} {resp.url} - {resp.status_code}') 
        if args.flag not in resp.json()[-1]['comments']:
            return CheckerResult(status=Status.CORRUPT.value, private_info='', public_info=f'PULL {Status.CORRUPT.value} {resp.url} - {resp.status_code}') 
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    return CheckerResult(status=Status.OK.value, private_info="журейка топ;)", public_info='PULL works')


if __name__ == '__main__':
    import sys
    action, *args = sys.argv[1:]
    result = None
    try:
        if action == 'push':
            host, round_number, flag = args
            push_args = PushArgs(host=host, round_number=round_number, flag=flag)
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
        print(result.public_info, file = sys.stderr)
    print(result.private_info)
    exit(result.status)
