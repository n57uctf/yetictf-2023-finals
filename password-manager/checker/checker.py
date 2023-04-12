from typing import NamedTuple
import requests, enum, typing, random, string, json


PORT = 8091
names = ('Aaberg', 'Abbot', 'Abernon', 'Abram', 'Ackerley', 'Adalbert', 'Adamsen', 'Ade', 'Ader', 'Adlare', 'Adore', 'Adrienne', 'Afton', 'Agle', 'Ahab', 'Aida', 'Ailyn', 'Ajay', 'Alabaster', 'Alarise', 'Albertine', 'Alcott', 'Aldric', 'Alejoa', 'Alexandr', 'Alfons', 'Alice', 'Alisia', 'Allare', 'Allina', 'Allys', 'Aloise', 'Alrich', 'Alva', 'Alwin', 'Amadas', 'Amand', 'Amasa', 'Ambrosia', 'Amethist', 'Ammann', 'Ana', 'Anastice', 'Anderegg', 'Andres', 'Anet', 'Angelita', 'Anissa', 'Annabelle', 'Annie', 'Anselmo', 'Antone', 'Anzovin', 'Aprilette', 'Arbe', 'Ardehs', 'Ardrey', 'Argyle', 'Arielle', 'Arleyne', 'Armando', 'Arnelle', 'Arratoon', 'Artima', 'Arvonio', 'Asher', 'Ashraf', 'Astraea', 'Athal', 'Atrice', 'Auberon', 'Audra', 'Augusta', 'Aurelius', 'Autry', 'Avictor', 'Axe', 'Aziza', 'Bachman', 'Baiel', 'Bakki', 'Ballard', 'Bander', 'Bar', 'Barbi', 'Barimah', 'Barnie', 'Barry', 'Bartley', 'Bashuk', 'Batha', 'Baudoin', 'Bayly', 'Beasley', 'Beberg', 'Beeck', 'Behrens', 'Belayneh', 'Belle', 'Bendicta', 'Benil', 'Bennink', 'Berardo', 'Bergmann', 'Berlauda', 'Bernelle', 'Berry', 'Bertolde', 'Bethel', 'Betty', 'Bevis', 'Bible', 'Bigod', 'Bilow', 'Birdie', 'Bixby', 'Blakelee', 'Blaseio', 'Blithe', 'Bluhm', 'Bobbette', 'Boehmer', 'Bohman', 'Bollen', 'Bonina', 'Booker', 'Borden', 'Borreri', 'Boucher', 'Bowden', 'Boycie', 'Brackett', 'Braeunig', 'Brandie', 'Braunstein', 'Breen', 'Brenna', 'Briana', 'Brietta', 'Bringhurst', 'Brittany', 'Broder', 'Bronnie', 'Brott', 'Brunella', 'Bryner', 'Buckley', 'Buffy', 'Bum', 'Burchett', 'Burkley', 'Burny', 'Busby', 'Butte', 'Byrom', 'Cadmarr', 'Caitrin', 'Calia', 'Calloway', 'Camel', 'Campbell', 'Candyce', 'Caplan', 'Carbone', 'Cargian', 'Carlen', 'Carlstrom', 'Carmencita', 'Carolina', 'Carrick', 'Cary', 'Casimire', 'Cassondra', 'Catha', 'Catima', 'Cavanagh', 'Ceciley', 'Celestyn', 'Centonze', 'Chace', 'Chak', 'Chandless', 'Chapman', 'Charla', 'Charmion', 'Chavaree', 'Chema', 'Cherice', 'Chesney', 'Chickie', 'Chiou', 'Chon', 'Christalle', 'Christis', 'Chu', 'Ciapha', 'Cinda', 'Cirone', 'Clarabelle', 'Clarisse', 'Claudio', 'Clein', 'Cleodal', 'Cliff', 'Close', 'Cnut', 'Codee', 'Cohe', 'Colburn', 'Collen', 'Colpin', 'Combe', 'Conchita', 'Conner', 'Constant', 'Cooley', 'Corabelle', 'Cordie', 'Corin', 'Cornelie', 'Corrinne', 'Cosetta', 'Cottrell', 'Covell', 'Craggy', 'Crean', 'Cressler', 'Cristian', 'Crompton', 'Cruickshank', 'Culliton', 'Currey', 'Cutlip', 'Cynara', 'Cyril', 'Dael', 'Dahlstrom', 'Dallis', 'Dambro', 'Danczyk', 'Daniell', 'Dante', 'Darby', 'Darice', 'Darrelle', 'Dasha', 'Davey', 'Dawn', 'Dearborn', 'Decato', 'Deedee', 'Dela', 'Delija', 'Delos', 'Deming', 'Denie', 'Denver', 'Dermot', 'Des', 'Deste', 'Devland', 'Dewitt', 'Dianemarie', 'Dich', 'Dielle', 'Dimitri', 'Dinsmore', 'Dittman', 'Docile', 'Doi', 'Dolphin', 'Dominus', 'Donela', 'Donny', 'Dorcus', 'Dorinda', 'Dorothi', 'Dosi', 'Douglas', 'Downs', 'Dream', 'Driskill', 'Drummond', 'Dudden', 'Dulcia', 'Dunham', 'Durant', 'Durward', 'Duvall', 'Dyanne', 'Eachelle', 'Earley', 'Ebby', 'Eckart', 'Edea', 'Edina', 'Edmonds', 'Edva', 'Egarton', 'Ehrlich', 'Eisenstark', 'Elberta', 'Eldreeda', 'Eleph', 'Eliathan', 'Elish', 'Ellerd', 'Ellora', 'Elnore', 'Elsie', 'Elvis', 'Emalia', 'Emersen', 'Emmalee', 'Emmuela', 'Eng', 'Ennis', 'Ephrayim', 'Erastus', 'Erica', 'Erland', 'Ermine', 'Erroll', 'Esma', 'Estell', 'Ethan', 'Etoile', 'Eugene', 'Euphemie', 'Evander', 'Evelyn', 'Evslin', 'Ezana', 'Fabio', 'Fadil', 'Fairman', 'Fanchon', 'Fari', 'Farny', 'Fasano', 'Faus', 'Fawnia', 'Fedak', 'Feldt', 'Feliza', 'Fenner', 'Feriga', 'Ferrel', 'Fia', 'Fiertz', 'Fillander', 'Fini', 'Firman', 'Fitzpatrick', 'Fleeman', 'Flip', 'Florin', 'Flss', 'Fonsie', 'Forras', 'Foskett', 'France', 'Francoise', 'Franz', 'Freda', 'Fredette', 'French', 'Friedberg', 'Frodeen', 'Fruma', 'Fullerton', 'Fusco', 'Gabrielle', 'Gahan', 'Galatia', 'Gamali', 'Garaway', 'Gare', 'Garlen', 'Garris', 'Gaspar', 'Gauldin', 'Gavrielle', 'Gayner', 'Gefen', 'Gemina', 'Genisia', 'Geoffry', 'Georglana', 'Gerfen', 'Germana', 'Gerstner', 'Gherardi', 'Gibb', 'Giesser', 'Gilberto', 'Gill', 'Gilmore', 'Ginny', 'Girardi', 'Giuditta', 'Gladis', 'Glenda', 'Glover', 'Godber', 'Goer', 'Goldin', 'Gomar', 'Goodden', 'Gordie', 'Gotcher', 'Gow', 'Graham', 'Granny', 'Graybill', 'Greenstein', 'Gregory', 'Greyso', 'Grimbald', 'Groark', 'Grosvenor', 'Gualterio', 'Guild', 'Gunilla', 'Gusba', 'Guthrey', 'Gwenora', 'Hachmann', 'Haerle', 'Haile', 'Haldane', 'Hall', 'Halpern', 'Hamid', 'Hamrnand', 'Hankins', 'Hanser', 'Hardan', 'Harim', 'Harms', 'Harriette', 'Hartmunn', 'Hasheem', 'Hatfield', 'Havener', 'Hayman', 'Hazen', 'Hebert', 'Hedvah', 'Heidie', 'Heise', 'Helenka', 'Helsie', 'Hendry', 'Henricks', 'Hepsiba', 'Hermann', 'Herrah', 'Hertz', 'Hess', 'Hewie', 'Hidie', 'Hilary', 'Hillegass', 'Hime', 'Hiroshi', 'Hoashis', 'Hoem', 'Hola', 'Hollinger', 'Holtorf', 'Honora', 'Horacio', 'Hortense', 'Hound', 'Howlond', 'Huberman', 'Hufnagel', 'Hulen', 'Hun', 'Hurless', 'Hutchinson', 'Hyde', 'Iaria', 'Idel', 'Ieso', 'Ihab', 'Ilise', 'Imelda', 'Infeld', 'Ingold', 'Iny', 'Iphigeniah', 'Irmina', 'Isac', 'Isidora', 'Israel', 'Ive', 'Iz', 'Jacie', 'Jacoba', 'Jacquette', 'Jaffe', 'Jala', 'Jamison', 'Janelle', 'Janis', 'Janyte', 'Jariah', 'Jarvis', 'Jaye', 'Jeanna', 'Jeffcott', 'Jehovah', 'Jen', 'Jennee', 'Jerad', 'Jerol', 'Jesher', 'Jeth', 'Jillana', 'JoAnne', 'Jobe', 'Jody', 'Johanan', 'Johns', 'Jolenta', 'Jones', 'Jordon', 'Joselow', 'Josselyn', 'Jozef', 'Judus', 'Julie', 'Juni', 'Justine', 'Kaela', 'Kaitlynn', 'Kalin', 'Kama', 'Kania', 'Karas', 'Karissa', 'Karlyn', 'Kary', 'Kassity', 'Katheryn', 'Katonah', 'Kaufmann', 'Kaz', 'Keeler', 'Keiko', 'Kelila', 'Kelsy', 'Kendrah', 'Kenneth', 'Kenwee', 'Kerman', 'Kery', 'Kevin', 'Khichabia', 'Kieran', 'Killian', 'Kimmel', 'Kingston', 'Kira', 'Kirsteni', 'Kitty', 'Klement', 'Klos', 'Knowle', 'Kobylak', 'Kolk', 'Konstantine', 'Korenblat', 'Kosel', 'Kowtko', 'Krause', 'Krenn', 'Kristel', 'Krock', 'Krystalle', 'Kumler', 'Kusin', 'Kyla', 'LaMee', 'Lachman', 'Lahey', 'Lali', 'Lammond', 'Lancelot', 'Landry', 'Langston', 'Laraine', 'Larkin', 'Lashondra', 'Latimer', 'Latt', 'Launcelot', 'Lauretta', 'Lavena', 'Lawson', 'LeMay', 'Leanora', 'Leclair', 'Leesen', 'Leid', 'Lela', 'Lemon', 'Lenno', 'Leon', 'Leontina', 'Leshia', 'Letizia', 'Leveridge', 'Lewellen', 'Lezlie', 'Libby', 'Lidia', 'Lila', 'Lily', 'Lindbom', 'Lindy', 'Linnie', 'Lipscomb', 'Liss', 'Liu', 'Lizzy', 'Lodmilla', 'Lolande', 'Longan', 'Lopes', 'Lorena', 'Lorinda', 'Lorry', 'Lotus', 'Loux', 'Lowney', 'Lubeck', 'Lucic', 'Lucy', 'Luelle', 'Lulita', 'Lunneta', 'Lustick', 'Lyford', 'Lynelle', 'Lysander', 'MacGregor', 'Maccarone', 'Macy', 'Madelaine', 'Madonia', 'Magda', 'Magna', 'Mahon', 'Maire', 'Malamud', 'Malia', 'Mallis', 'Malvie', 'Mandi', 'Manny', 'Manya', 'Marcellina', 'Marcoux', 'Margalo', 'Margit', 'Mariano', 'Marigolde', 'Marion', 'Market', 'Marler', 'Maro', 'Marrissa', 'Martelli', 'Martinson', 'Marya', 'Marysa', 'Mastic', 'Mathian', 'Matthaus', 'Maud', 'Maurili', 'Maxentia', 'Mayce', 'Mazonson', 'McClelland', 'McCullough', 'McGraw', 'McKinney', 'McNeely', 'Meaghan', 'Medora', 'Meghan', 'Mela', 'Melessa', 'Mella', 'Melody', 'Mendelsohn', 'Meraree', 'Meredi', 'Merlin', 'Merrill', 'Meta', 'Micaela', 'Michelina', 'Middendorf', 'Mikael', 'Milburr', 'Millar', 'Milon', 'Miner', 'Minta', 'Mirilla', 'Mitinger', 'Modeste', 'Mohr', 'Molly', 'Monika', 'Monteith', 'Mord', 'Morganne', 'Morra', 'Mosa', 'Mossman', 'Moyna', 'Mulcahy', 'Munford', 'Murdock', 'Muslim', 'Myra', 'Naamana', 'Nadean', 'Nahshu', 'Names', 'Nanny', 'Nari', 'Natal', 'Nathanial', 'Nazar', 'Neddy', 'Neile', 'Nellir', 'Neri', 'Nessie', 'Neumark', 'Newby', 'Niall', 'Nicki', 'Nicolella', 'Nightingale', 'Nikos', 'Niobe', 'Noach', 'Noell', 'Nollie', 'Nord', 'Normi', 'Norvell', 'Nozicka', 'Nyhagen', 'Obau', 'Obrien', 'Odele', 'Odom', 'Ogg', 'Olatha', 'Olga', 'Olly', 'Olympe', 'Ondine', 'Oona', 'Orbadiah', 'Orgell', 'Orlando', 'Ornstead', 'Orthman', 'Osborn', 'Ossie', 'Othelia', 'Otto', 'Ozzie', "O'Meara", 'Packer', 'Paige', 'Palma', 'Panayiotis', 'Paola', 'Pardoes', 'Parrish', 'Pascale', 'Patience', 'Patterman', 'Paulita', 'Paxton', 'Pearlman', 'Pedroza', 'Pelaga', 'Pena', 'Pentha', 'Per', 'Perloff', 'Perseus', 'Peterson', 'Petronilla', 'Pfeifer', 'Phene', 'Philine', 'Phillis', 'Phox', 'Piefer', 'Pike', 'Pinter', 'Piselli', 'Plante', 'Plumbo', 'Polito', 'Pomona', 'Popelka', 'Portwine', 'Power', 'Prendergast', 'Priebe', 'Prissie', 'Proudfoot', 'Pryor', 'Pulcheria', 'Puto', 'Queenie', 'Quince', 'Quiteris', 'Rachel', 'Radloff', 'Raffaello', 'Rahr', 'Rakia', 'Ramey', 'Randal', 'Ranit', 'Rapp', 'Ratib', 'Ray', 'Rayshell', 'Rebbecca', 'Redfield', 'Reeva', 'Reiche', 'Reinhard', 'Rem', 'Rene', 'Renwick', 'Reuven', 'Rhea', 'Rhodie', 'Ribble', 'Richela', 'Ricker', 'Riegel', 'Riki', 'Rintoul', 'Ritchie', 'Roana', 'Robert', 'Robyn', 'Rockie', 'Rodie', 'Roer', 'Rolando', 'Romanas', 'Romonda', 'Ronny', 'Rosa', 'Rosanne', 'Rosemare', 'Rosenthal', 'Rossen', 'Rothwell', 'Rowney', 'Roz', 'Ruberta', 'Rudin', 'Rufford', 'Ruperta', 'Russo', 'Ruthy', 'Saba', 'Sachi', 'Sadler', 'Saied', 'Salas', 'Sallee', 'Salvador', 'Sami', 'Sanborne', 'Sandry', 'Santa', 'Sarajane', 'Sartin', 'Saum', 'Savior', 'Saylor', 'Schaeffer', 'Scheider', 'Schlesinger', 'Schoening', 'Schriever', 'Schwartz', 'Scotti', 'Seaden', 'Sebastiano', 'Seem', 'Seiter', 'Selhorst', 'Selmner', 'Seow', 'Sergius', 'Seto', 'Seymour', 'Shakti', 'Shanie', 'Shargel', 'Shaughnessy', 'Shear', 'Shel', 'Shelton', 'Shere', 'Sherr', 'Sheya', 'Shippee', 'Shoifet', 'Shue', 'Shute', 'Sibley', 'Sidon', 'Siesser', 'Sik', 'Silsby', 'Simah', 'Sinclair', 'Sirotek', 'Skantze', 'Skipton', 'Slayton', 'Smart', 'So', 'Solberg', 'Sommer', 'Sophey', 'Sosna', 'Spalla', 'Spence', 'Spohr', 'Stacey', 'Stan', 'Stanton', 'Staten', 'Steele', 'Steinke', 'Stephenie', 'Stevena', 'Stillas', 'Stoecker', 'Stouffer', 'Streetman', 'Stroup', 'Stutsman', 'Sugihara', 'Sunda', 'Susana', 'Suzan', 'Swamy', 'Swetlana', 'Sybille', 'Synn', 'Tace', 'Taggart', 'Talbert', 'Tam', 'Tammie', 'Tannenbaum', 'Tarr', 'Tate', 'Tawney', 'Tedda', 'Tegan', 'Ten', 'Terbecki', 'Terrance', 'Tertia', 'Tews', 'Thanh', 'Thedrick', 'Therese', 'Thibaut', 'Thomajan', 'Thorma', 'Three', 'Tibbitts', 'Tiertza')
service_name = ('Telegram', 'Vkontakte', 'Youtube', 'Одноклассники', 'Instagram', 'Facebook', 'Дзен', 'ЯRus', 'Tenchat', 'GitHub', 'Whatsapp', 'Ok.ru', 'Gmail.com', 'Mail.ru', 'TryHackMe', 'DuckDuckGo', 'Yandex')


def get_random_name():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(10000, 99999))


def get_random_service_name():
    """
    Генерация рандомного имени сервиса для пароля сохраненного
    """
    ran = len(service_name)
    service = service_name[random.randint(0, ran - 1)]
    return service


def get_password():
    """
    Генерация рандомного пароля для регистрации
    """
    password = []
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    for i in range(20):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


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


def get_json(response, validate_response=True):
    """
    Проверка полученного json
    """
    try:
        data = json.loads(response.text)
    except:
        CheckerResult(status=Status.MUMBLE.value,
                      private_info=f'JSON validation error on url: {response.url}',
                      public_info=f'JSON validation error on url: {response.url}, content: {response.text}')
    if not validate_response:
        return data
    try:
        if response.status_code == 200:
            return data
        else:
            CheckerResult(status=Status.MUMBLE.value,
                          private_info=f'Response status not success on url: {response.url}',
                          public_info=f'Response status not success on url: {response.url}, content: {response.text}')
    except:
        CheckerResult(status=Status.MUMBLE.value,
                      private_info=f'Unknown response status ("success" field in response not found), url: {response.url}',
                      public_info=f'Unknown response status ("success" field in response not found), url: {response.url}, content: {response.text}')


def push(args: PushArgs) -> CheckerResult:
    """
    Функция PUSH
    """
    url = f'http://{args.host}:{PORT}/api'

    # Check push
    # Connect
    try:
        r = requests.get(f"{url}/get_users")
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                private_info=f'{r.status_code}',
                                public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.DOWN.value} Can not connect')

    try:
        creds = {"username": get_random_name(), "password": get_password()}
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.ERROR.value} checker can not generate creds')

    res = CheckerResult(status=Status.OK.value,
                        private_info=json.dumps(creds),
                        public_info='PUSH works')

    # Get Users
    try:
        r = requests.get(f'{url}/get_users')
        print(r.status_code, r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not get users list: {r.url}, content: {r.text}')

    # Register
    try:
        r = requests.post(f'{url}/register', json=creds)
        print(r.status_code, r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not register user: {r.url}, content: {r.text}')

    # Login
    try:
        r = requests.post(f'{url}/login', json=creds)
        print(r.status_code, r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
        token = data["token"]
        print(token)
        auth_header = {'Authorization': f'Bearer {token}'}
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not login: {r.url}, content: {r.text}')

    # Get Profile data
    try:
        r = requests.get(f'{url}/profile', headers=auth_header)
        print(r.status_code, r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
        master_password = data["masterpass"]
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not get profile data: {r.url}, content: {r.text}')

    # Get Storage data
    try:
        r = requests.get(f'{url}/storage', headers=auth_header)
        print(r.status_code, r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not get storage data: {r.url}, content: {r.text}')

    # Add new password to storage
    try:
        r = requests.post(f'{url}/storage', headers=auth_header,
                          json={"password": args.flag, "title": get_random_service_name()})
        print("response", r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        if r.json()["password"] != args.flag:
            return CheckerResult(status=Status.CORRUPT.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.CORRUPT.value} Can not store flag')
        data = get_json(r)
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not add password to storage: {r.url}, content: {r.text}')

    # Create share Link for password
    try:
        r = requests.get(f'{url}/share?record_id={data["record_id"]}', headers=auth_header)
        print("response", r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
        # Check if link works
        r = requests.get(f'{url}/shared_link?shared_password_link={data["link"]}')
        print("response", r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} can not create share link: {r.url}, content: {r.text}')

    # Download backup storage
    try:
        r = requests.get(f'{url}/export?username={creds["username"]}')
        print("response", r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        data = get_json(r)
        r = requests.get(f'{url}/file?link={data["link"]}')
        print("response-file", r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
        print(master_password)
        r = requests.post(f'{url}/decrypt', json={"master_password": master_password, "data": r.text})
        print("response-decrypt", r.json()["data"])
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                            private_info=str(e),
                            public_info=f'PUSH {Status.MUMBLE.value} create backup not working: {r.url}, content: {r.text}')

    return res
"""
    resp = requests.post(f'http://{args.host}:{PORT}/put', json={'id':args.round_number, 'flag': args.flag})
    if resp.status_code != 200:
        return CheckerResult(status=Status.MUMBLE.value, private_info='', public_info=f'PUSH {Status.MUMBLE.value} {resp.url} - {resp.status_code}')
    if resp.json()['flag'] != args.flag:
        return CheckerResult(status=Status.CORRUPT.value, private_info='', public_info=f'PUSH {Status.CORRUPT.value} Can not store flag')
"""


def pull(args: PullArgs) -> CheckerResult:
    res = CheckerResult(status=Status.OK.value,
                        private_info=str(args.private_info),
                        public_info='PULL works')
    url = f'http://{args.host}:{PORT}/api'

    # Login
    try:
        r = requests.post(f'{url}/login', json=json.loads(args.private_info))
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                private_info=str(args.private_info),
                                public_info=f'PULL {Status.MUMBLE.value} can not login {r.url} - {r.status_code}')
        data = get_json(r)
        token = data["token"]
        print(token)
        auth_header = {'Authorization': f'Bearer {token}'}
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                             private_info=str(e),
                             public_info=f'PULL {Status.MUMBLE.value} can not login: {r.url}, content: {r.text}')

    # Check Flag
    try:
        r = requests.get(f'{url}/storage', headers=auth_header)
        print(r.status_code, r.text)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PULL {Status.MUMBLE.value} can not get flag: {r.url}, content: {r.text}')
        data = get_json(r)
        if data[0]['password'] != args.flag:
            return CheckerResult(status=Status.CORRUPT.value,
                                 private_info=str(args.private_info),
                                 public_info=f'PULL {Status.CORRUPT.value} Flags do not match: {r.url}, content: {r.text}')
    except Exception as e:
        return CheckerResult(status=Status.MUMBLE.value,
                             private_info=str(e),
                             public_info=f'PULL {Status.MUMBLE.value} flags dont match: {r.url}, content: {r.text}')
    return res


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
        print(result.public_info, file = sys.stderr)
    print(result.private_info)
    exit(result.status)
