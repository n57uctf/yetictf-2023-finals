import re
import string
from typing import NamedTuple  # Делаем обязательный импорт
import requests
import enum
import random
import typing
import os
import base64
import json

agents = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.1; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
]

def rnd_agent():
    return random.choice(agents)


PORT = 1111

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
    private_info: list
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
    private_info: list  # приватные данные которые чекер вернул когда клал флаг
    flag: str  # Флаг который нужно получить из сервиса


def get_random_password(dlina):
    pas = ''
    for x in range(dlina):  # Количество символов (16)
        pas = pas + random.choice(list(
            '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))  # Символы, из которых будет составлен пароль
    return pas


def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_random_name():
    names = ('Aaberg', 'Abbot', 'Abernon', 'Abram', 'Ackerley', 'Adalbert', 'Adamsen', 'Ade', 'Ader', 'Adlare', 'Adore',
             'Adrienne', 'Afton', 'Agle', 'Ahab', 'Aida', 'Ailyn', 'Ajay', 'Alabaster', 'Alarise', 'Albertine',
             'Alcott', 'Aldric', 'Alejoa', 'Alexandr', 'Alfons', 'Alice', 'Alisia', 'Allare', 'Allina', 'Allys',
             'Aloise', 'Alrich', 'Alva', 'Alwin', 'Amadas', 'Amand', 'Amasa', 'Ambrosia', 'Amethist', 'Ammann', 'Ana',
             'Anastice', 'Anderegg', 'Andres', 'Anet', 'Angelita', 'Anissa', 'Annabelle', 'Annie', 'Anselmo', 'Antone',
             'Anzovin', 'Aprilette', 'Arbe', 'Ardehs', 'Ardrey', 'Argyle', 'Arielle', 'Arleyne', 'Armando', 'Arnelle',
             'Arratoon', 'Artima', 'Arvonio', 'Asher', 'Ashraf', 'Astraea', 'Athal', 'Atrice', 'Auberon', 'Audra',
             'Augusta', 'Aurelius', 'Autry', 'Avictor', 'Axe', 'Aziza', 'Bachman', 'Baiel', 'Bakki', 'Ballard',
             'Bander', 'Bar', 'Barbi', 'Barimah', 'Barnie', 'Barry', 'Bartley', 'Bashuk', 'Batha', 'Baudoin', 'Bayly',
             'Beasley', 'Beberg', 'Beeck', 'Behrens', 'Belayneh', 'Belle', 'Bendicta', 'Benil', 'Bennink', 'Berardo',
             'Bergmann', 'Berlauda', 'Bernelle', 'Berry', 'Bertolde', 'Bethel', 'Betty', 'Bevis', 'Bible', 'Bigod',
             'Bilow', 'Birdie', 'Bixby', 'Blakelee', 'Blaseio', 'Blithe', 'Bluhm', 'Bobbette', 'Boehmer', 'Bohman',
             'Bollen', 'Bonina', 'Booker', 'Borden', 'Borreri', 'Boucher', 'Bowden', 'Boycie', 'Brackett', 'Braeunig',
             'Brandie', 'Braunstein', 'Breen', 'Brenna', 'Briana', 'Brietta', 'Bringhurst', 'Brittany', 'Broder',
             'Bronnie', 'Brott', 'Brunella', 'Bryner', 'Buckley', 'Buffy', 'Bum', 'Burchett', 'Burkley', 'Burny',
             'Busby', 'Butte', 'Byrom', 'Cadmarr', 'Caitrin', 'Calia', 'Calloway', 'Camel', 'Campbell', 'Candyce',
             'Caplan', 'Carbone', 'Cargian', 'Carlen', 'Carlstrom', 'Carmencita', 'Carolina', 'Carrick', 'Cary',
             'Casimire', 'Cassondra', 'Catha', 'Catima', 'Cavanagh', 'Ceciley', 'Celestyn', 'Centonze', 'Chace', 'Chak',
             'Chandless', 'Chapman', 'Charla', 'Charmion', 'Chavaree', 'Chema', 'Cherice', 'Chesney', 'Chickie',
             'Chiou', 'Chon', 'Christalle', 'Christis', 'Chu', 'Ciapha', 'Cinda', 'Cirone', 'Clarabelle', 'Clarisse',
             'Claudio', 'Clein', 'Cleodal', 'Cliff', 'Close', 'Cnut', 'Codee', 'Cohe', 'Colburn', 'Collen', 'Colpin',
             'Combe', 'Conchita', 'Conner', 'Constant', 'Cooley', 'Corabelle', 'Cordie', 'Corin', 'Cornelie',
             'Corrinne', 'Cosetta', 'Cottrell', 'Covell', 'Craggy', 'Crean', 'Cressler', 'Cristian', 'Crompton',
             'Cruickshank', 'Culliton', 'Currey', 'Cutlip', 'Cynara', 'Cyril', 'Dael', 'Dahlstrom', 'Dallis', 'Dambro',
             'Danczyk', 'Daniell', 'Dante', 'Darby', 'Darice', 'Darrelle', 'Dasha', 'Davey', 'Dawn', 'Dearborn',
             'Decato', 'Deedee', 'Dela', 'Delija', 'Delos', 'Deming', 'Denie', 'Denver', 'Dermot', 'Des', 'Deste',
             'Devland', 'Dewitt', 'Dianemarie', 'Dich', 'Dielle', 'Dimitri', 'Dinsmore', 'Dittman', 'Docile', 'Doi',
             'Dolphin', 'Dominus', 'Donela', 'Donny', 'Dorcus', 'Dorinda', 'Dorothi', 'Dosi', 'Douglas', 'Downs',
             'Dream', 'Driskill', 'Drummond', 'Dudden', 'Dulcia', 'Dunham', 'Durant', 'Durward', 'Duvall', 'Dyanne',
             'Eachelle', 'Earley', 'Ebby', 'Eckart', 'Edea', 'Edina', 'Edmonds', 'Edva', 'Egarton', 'Ehrlich',
             'Eisenstark', 'Elberta', 'Eldreeda', 'Eleph', 'Eliathan', 'Elish', 'Ellerd', 'Ellora', 'Elnore', 'Elsie',
             'Elvis', 'Emalia', 'Emersen', 'Emmalee', 'Emmuela', 'Eng', 'Ennis', 'Ephrayim', 'Erastus', 'Erica',
             'Erland', 'Ermine', 'Erroll', 'Esma', 'Estell', 'Ethan', 'Etoile', 'Eugene', 'Euphemie', 'Evander',
             'Evelyn', 'Evslin', 'Ezana', 'Fabio', 'Fadil', 'Fairman', 'Fanchon', 'Fari', 'Farny', 'Fasano', 'Faus',
             'Fawnia', 'Fedak', 'Feldt', 'Feliza', 'Fenner', 'Feriga', 'Ferrel', 'Fia', 'Fiertz', 'Fillander', 'Fini',
             'Firman', 'Fitzpatrick', 'Fleeman', 'Flip', 'Florin', 'Flss', 'Fonsie', 'Forras', 'Foskett', 'France',
             'Francoise', 'Franz', 'Freda', 'Fredette', 'French', 'Friedberg', 'Frodeen', 'Fruma', 'Fullerton', 'Fusco',
             'Gabrielle', 'Gahan', 'Galatia', 'Gamali', 'Garaway', 'Gare', 'Garlen', 'Garris', 'Gaspar', 'Gauldin',
             'Gavrielle', 'Gayner', 'Gefen', 'Gemina', 'Genisia', 'Geoffry', 'Georglana', 'Gerfen', 'Germana',
             'Gerstner', 'Gherardi', 'Gibb', 'Giesser', 'Gilberto', 'Gill', 'Gilmore', 'Ginny', 'Girardi', 'Giuditta',
             'Gladis', 'Glenda', 'Glover', 'Godber', 'Goer', 'Goldin', 'Gomar', 'Goodden', 'Gordie', 'Gotcher', 'Gow',
             'Graham', 'Granny', 'Graybill', 'Greenstein', 'Gregory', 'Greyso', 'Grimbald', 'Groark', 'Grosvenor',
             'Gualterio', 'Guild', 'Gunilla', 'Gusba', 'Guthrey', 'Gwenora', 'Hachmann', 'Haerle', 'Haile', 'Haldane',
             'Hall', 'Halpern', 'Hamid', 'Hamrnand', 'Hankins', 'Hanser', 'Hardan', 'Harim', 'Harms', 'Harriette',
             'Hartmunn', 'Hasheem', 'Hatfield', 'Havener', 'Hayman', 'Hazen', 'Hebert', 'Hedvah', 'Heidie', 'Heise',
             'Helenka', 'Helsie', 'Hendry', 'Henricks', 'Hepsiba', 'Hermann', 'Herrah', 'Hertz', 'Hess', 'Hewie',
             'Hidie', 'Hilary', 'Hillegass', 'Hime', 'Hiroshi', 'Hoashis', 'Hoem', 'Hola', 'Hollinger', 'Holtorf',
             'Honora', 'Horacio', 'Hortense', 'Hound', 'Howlond', 'Huberman', 'Hufnagel', 'Hulen', 'Hun', 'Hurless',
             'Hutchinson', 'Hyde', 'Iaria', 'Idel', 'Ieso', 'Ihab', 'Ilise', 'Imelda', 'Infeld', 'Ingold', 'Iny',
             'Iphigeniah', 'Irmina', 'Isac', 'Isidora', 'Israel', 'Ive', 'Iz', 'Jacie', 'Jacoba', 'Jacquette', 'Jaffe',
             'Jala', 'Jamison', 'Janelle', 'Janis', 'Janyte', 'Jariah', 'Jarvis', 'Jaye', 'Jeanna', 'Jeffcott',
             'Jehovah', 'Jen', 'Jennee', 'Jerad', 'Jerol', 'Jesher', 'Jeth', 'Jillana', 'JoAnne', 'Jobe', 'Jody',
             'Johanan', 'Johns', 'Jolenta', 'Jones', 'Jordon', 'Joselow', 'Josselyn', 'Jozef', 'Judus', 'Julie', 'Juni',
             'Justine', 'Kaela', 'Kaitlynn', 'Kalin', 'Kama', 'Kania', 'Karas', 'Karissa', 'Karlyn', 'Kary', 'Kassity',
             'Katheryn', 'Katonah', 'Kaufmann', 'Kaz', 'Keeler', 'Keiko', 'Kelila', 'Kelsy', 'Kendrah', 'Kenneth',
             'Kenwee', 'Kerman', 'Kery', 'Kevin', 'Khichabia', 'Kieran', 'Killian', 'Kimmel', 'Kingston', 'Kira',
             'Kirsteni', 'Kitty', 'Klement', 'Klos', 'Knowle', 'Kobylak', 'Kolk', 'Konstantine', 'Korenblat', 'Kosel',
             'Kowtko', 'Krause', 'Krenn', 'Kristel', 'Krock', 'Krystalle', 'Kumler', 'Kusin', 'Kyla', 'LaMee',
             'Lachman', 'Lahey', 'Lali', 'Lammond', 'Lancelot', 'Landry', 'Langston', 'Laraine', 'Larkin', 'Lashondra',
             'Latimer', 'Latt', 'Launcelot', 'Lauretta', 'Lavena', 'Lawson', 'LeMay', 'Leanora', 'Leclair', 'Leesen',
             'Leid', 'Lela', 'Lemon', 'Lenno', 'Leon', 'Leontina', 'Leshia', 'Letizia', 'Leveridge', 'Lewellen',
             'Lezlie', 'Libby', 'Lidia', 'Lila', 'Lily', 'Lindbom', 'Lindy', 'Linnie', 'Lipscomb', 'Liss', 'Liu',
             'Lizzy', 'Lodmilla', 'Lolande', 'Longan', 'Lopes', 'Lorena', 'Lorinda', 'Lorry', 'Lotus', 'Loux', 'Lowney',
             'Lubeck', 'Lucic', 'Lucy', 'Luelle', 'Lulita', 'Lunneta', 'Lustick', 'Lyford', 'Lynelle', 'Lysander',
             'MacGregor', 'Maccarone', 'Macy', 'Madelaine', 'Madonia', 'Magda', 'Magna', 'Mahon', 'Maire', 'Malamud',
             'Malia', 'Mallis', 'Malvie', 'Mandi', 'Manny', 'Manya', 'Marcellina', 'Marcoux', 'Margalo', 'Margit',
             'Mariano', 'Marigolde', 'Marion', 'Market', 'Marler', 'Maro', 'Marrissa', 'Martelli', 'Martinson', 'Marya',
             'Marysa', 'Mastic', 'Mathian', 'Matthaus', 'Maud', 'Maurili', 'Maxentia', 'Mayce', 'Mazonson',
             'McClelland', 'McCullough', 'McGraw', 'McKinney', 'McNeely', 'Meaghan', 'Medora', 'Meghan', 'Mela',
             'Melessa', 'Mella', 'Melody', 'Mendelsohn', 'Meraree', 'Meredi', 'Merlin', 'Merrill', 'Meta', 'Micaela',
             'Michelina', 'Middendorf', 'Mikael', 'Milburr', 'Millar', 'Milon', 'Miner', 'Minta', 'Mirilla', 'Mitinger',
             'Modeste', 'Mohr', 'Molly', 'Monika', 'Monteith', 'Mord', 'Morganne', 'Morra', 'Mosa', 'Mossman', 'Moyna',
             'Mulcahy', 'Munford', 'Murdock', 'Muslim', 'Myra', 'Naamana', 'Nadean', 'Nahshu', 'Names', 'Nanny', 'Nari',
             'Natal', 'Nathanial', 'Nazar', 'Neddy', 'Neile', 'Nellir', 'Neri', 'Nessie', 'Neumark', 'Newby', 'Niall',
             'Nicki', 'Nicolella', 'Nightingale', 'Nikos', 'Niobe', 'Noach', 'Noell', 'Nollie', 'Nord', 'Normi',
             'Norvell', 'Nozicka', 'Nyhagen', 'Obau', 'Obrien', 'Odele', 'Odom', 'Ogg', 'Olatha', 'Olga', 'Olly',
             'Olympe', 'Ondine', 'Oona', 'Orbadiah', 'Orgell', 'Orlando', 'Ornstead', 'Orthman', 'Osborn', 'Ossie',
             'Othelia', 'Otto', 'Ozzie', "O'Meara", 'Packer', 'Paige', 'Palma', 'Panayiotis', 'Paola', 'Pardoes',
             'Parrish', 'Pascale', 'Patience', 'Patterman', 'Paulita', 'Paxton', 'Pearlman', 'Pedroza', 'Pelaga',
             'Pena', 'Pentha', 'Per', 'Perloff', 'Perseus', 'Peterson', 'Petronilla', 'Pfeifer', 'Phene', 'Philine',
             'Phillis', 'Phox', 'Piefer', 'Pike', 'Pinter', 'Piselli', 'Plante', 'Plumbo', 'Polito', 'Pomona',
             'Popelka', 'Portwine', 'Power', 'Prendergast', 'Priebe', 'Prissie', 'Proudfoot', 'Pryor', 'Pulcheria',
             'Puto', 'Queenie', 'Quince', 'Quiteris', 'Rachel', 'Radloff', 'Raffaello', 'Rahr', 'Rakia', 'Ramey',
             'Randal', 'Ranit', 'Rapp', 'Ratib', 'Ray', 'Rayshell', 'Rebbecca', 'Redfield', 'Reeva', 'Reiche',
             'Reinhard', 'Rem', 'Rene', 'Renwick', 'Reuven', 'Rhea', 'Rhodie', 'Ribble', 'Richela', 'Ricker', 'Riegel',
             'Riki', 'Rintoul', 'Ritchie', 'Roana', 'Robert', 'Robyn', 'Rockie', 'Rodie', 'Roer', 'Rolando', 'Romanas',
             'Romonda', 'Ronny', 'Rosa', 'Rosanne', 'Rosemare', 'Rosenthal', 'Rossen', 'Rothwell', 'Rowney', 'Roz',
             'Ruberta', 'Rudin', 'Rufford', 'Ruperta', 'Russo', 'Ruthy', 'Saba', 'Sachi', 'Sadler', 'Saied', 'Salas',
             'Sallee', 'Salvador', 'Sami', 'Sanborne', 'Sandry', 'Santa', 'Sarajane', 'Sartin', 'Saum', 'Savior',
             'Saylor', 'Schaeffer', 'Scheider', 'Schlesinger', 'Schoening', 'Schriever', 'Schwartz', 'Scotti', 'Seaden',
             'Sebastiano', 'Seem', 'Seiter', 'Selhorst', 'Selmner', 'Seow', 'Sergius', 'Seto', 'Seymour', 'Shakti',
             'Shanie', 'Shargel', 'Shaughnessy', 'Shear', 'Shel', 'Shelton', 'Shere', 'Sherr', 'Sheya', 'Shippee',
             'Shoifet', 'Shue', 'Shute', 'Sibley', 'Sidon', 'Siesser', 'Sik', 'Silsby', 'Simah', 'Sinclair', 'Sirotek',
             'Skantze', 'Skipton', 'Slayton', 'Smart', 'So', 'Solberg', 'Sommer', 'Sophey', 'Sosna', 'Spalla', 'Spence',
             'Spohr', 'Stacey', 'Stan', 'Stanton', 'Staten', 'Steele', 'Steinke', 'Stephenie', 'Stevena', 'Stillas',
             'Stoecker', 'Stouffer', 'Streetman', 'Stroup', 'Stutsman', 'Sugihara', 'Sunda', 'Susana', 'Suzan', 'Swamy',
             'Swetlana', 'Sybille', 'Synn', 'Tace', 'Taggart', 'Talbert', 'Tam', 'Tammie', 'Tannenbaum', 'Tarr', 'Tate',
             'Tawney', 'Tedda', 'Tegan', 'Ten', 'Terbecki', 'Terrance', 'Tertia', 'Tews', 'Thanh', 'Thedrick',
             'Therese', 'Thibaut', 'Thomajan', 'Thorma', 'Three', 'Tibbitts', 'Tiertza')
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(10000, 99999))


def push(args: PushArgs) -> CheckerResult:
    login = get_random_name()
    passwordik = get_random_password(16)
    try:
        r1 = requests.post(f'http://{args.host}:{PORT}/register',
                           data={'inputName': login, 'inputPassword': passwordik, 'inputConfirmPassword': passwordik},
                           allow_redirects=False, headers={'User-Agent': rnd_agent()}, timeout=5)
        r2 = requests.post(f'http://{args.host}:{PORT}/login', data={'inputName': login, 'inputPassword': passwordik},
                           allow_redirects=False, headers={'User-Agent': rnd_agent()}, timeout=5)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
    if r2.status_code != 302:
        return CheckerResult(status=Status.MUMBLE.value, private_info='',
                             public_info=f'PUSH {Status.MUMBLE.value} {r2.url} - {r2.status_code}')
    # ADD ENVIRON FOR ACTION
    place = 0
    if "PUSH_PLACE" in os.environ:
        place = int(os.environ.get("PUSH_PLACE"))
    else:
        place = random.randint(0, 8679) % 2

    if place == 0:
        try:
            r3 = requests.post(f'http://{args.host}:{PORT}/user', cookies={'Cookies': r2.cookies['Cookies']},
                               data={'inputPrivatbio': args.flag}, headers={'User-Agent': rnd_agent()}, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
        if r3.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r3.url} - {r3.status_code}')
        if args.flag not in r3.text:
            return CheckerResult(status=Status.CORRUPT.value, private_info='',
                                 public_info=f'PUSH {Status.CORRUPT.value} Can not store flag')
        private_info = json.dumps({'Cookies': str(r2.cookies['Cookies']), 'place': place})
        return CheckerResult(status=Status.OK.value, private_info=base64.b64encode(private_info.encode()).decode(),
                             public_info='PUSH works')
    else:
        try:
            r3 = requests.post(f'http://{args.host}:{PORT}/', cookies={'Cookies': r2.cookies['Cookies']},
                               data={'isPublic': False, 'groupName': get_random_string(),
                                     'groupDescription': get_random_string()}, headers={'User-Agent': rnd_agent()}, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
        if r3.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r3.url} - {r3.status_code}')
        group_id = re.findall(r'/group/quit/[0-9]+', r3.text)[0][12:]
        try:
            r4 = requests.post(f'http://{args.host}:{PORT}/group/{group_id}', cookies={'Cookies': r2.cookies['Cookies']},
                               data={'threadName': get_random_string(), 'threadDescription': get_random_string()}, headers={'User-Agent': rnd_agent()}, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
        if r4.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r4.url} - {r4.status_code}')
        thread_id = re.findall(r'/thread/[0-9]+', r4.text)[0][8:]
        try:
            r5 = requests.post(f'http://{args.host}:{PORT}/thread/{thread_id}', cookies={'Cookies': r2.cookies['Cookies']},
                               data={'addComment': args.flag}, headers={'User-Agent': rnd_agent()}, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
        if r5.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info='',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r5.url} - {r5.status_code}')
        if args.flag not in r5.text:
            return CheckerResult(status=Status.CORRUPT.value, private_info='',
                                 public_info=f'PUSH {Status.CORRUPT.value} Can not store flag')
        private_info = json.dumps({'Cookies': str(r2.cookies['Cookies']), 'place': place, 'thread_id': thread_id})
        return CheckerResult(status=Status.OK.value, private_info=base64.b64encode(private_info.encode()).decode(),
                             public_info='PUSH works')


def pull(args: PullArgs) -> CheckerResult:
    private_info = json.loads(base64.b64decode(args.private_info).decode())
    if private_info['place'] == 0:
        try:
            r1 = requests.get(f'http://{args.host}:{PORT}/user', cookies={'Cookies': private_info['Cookies']}, headers={'User-Agent': rnd_agent()}, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
        if r1.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info=private_info,
                                 public_info=f'PULL {Status.MUMBLE.value} {r1.url} - {r1.status_code}')
        if f'>{args.flag}<' not in r1.text:
            return CheckerResult(status=Status.CORRUPT.value, private_info=private_info,
                                 public_info=f'PULL {Status.CORRUPT.value} Can not pull flag')
        return CheckerResult(status=Status.OK.value, private_info=private_info, public_info='PULL works')
    else:
        try:
            r1 = requests.get(f'http://{args.host}:{PORT}/thread/{private_info["thread_id"]}',
                              cookies={'Cookies': private_info['Cookies']}, headers={'User-Agent': rnd_agent()}, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            return CheckerResult(status=Status.DOWN.value, private_info="", public_info="Connection error")
        if r1.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value, private_info=private_info,
                                 public_info=f'PULL {Status.MUMBLE.value} {r1.url} - {r1.status_code}')
        if f'>{args.flag}<' not in r1.text:
            return CheckerResult(status=Status.CORRUPT.value, private_info=private_info,
                                 public_info=f'PULL {Status.CORRUPT.value} Can not pull flag')
        return CheckerResult(status=Status.OK.value, private_info=private_info, public_info='PULL works')


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
        result = CheckerResult(status=Status.ERROR.value, private_info='', public_info=str(e))
    if result.status != Status.OK.value:
        print(result.public_info, file=sys.stderr)
    print(result.private_info)
    exit(result.status)
