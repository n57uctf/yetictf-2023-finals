"""
Checker
"""
import base64
import enum
import json
import os
import random
import re
import string
from io import BytesIO
from typing import NamedTuple

import pytesseract
import requests
from PIL import Image


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


PORT = 5555
names = (
    'Aaberg', 'Abbot', 'Abernon', 'Abram', 'Ackerley', 'Adalbert', 'Adamsen', 'Ade', 'Ader', 'Adlare', 'Adore',
    'Adrienne',
    'Afton', 'Agle', 'Ahab', 'Aida', 'Ailyn', 'Ajay', 'Alabaster', 'Alarise', 'Albertine', 'Alcott', 'Aldric', 'Alejoa',
    'Alexandr', 'Alfons', 'Alice', 'Alisia', 'Allare', 'Allina', 'Allys', 'Aloise', 'Alrich', 'Alva', 'Alwin', 'Amadas',
    'Amand', 'Amasa', 'Ambrosia', 'Amethist', 'Ammann', 'Ana', 'Anastice', 'Anderegg', 'Andres', 'Anet', 'Angelita',
    'Anissa', 'Annabelle', 'Annie', 'Anselmo', 'Antone', 'Anzovin', 'Aprilette', 'Arbe', 'Ardehs', 'Ardrey', 'Argyle',
    'Arielle', 'Arleyne', 'Armando', 'Arnelle', 'Arratoon', 'Artima', 'Arvonio', 'Asher', 'Ashraf', 'Astraea', 'Athal',
    'Atrice', 'Auberon', 'Audra', 'Augusta', 'Aurelius', 'Autry', 'Avictor', 'Axe', 'Aziza', 'Bachman', 'Baiel',
    'Bakki',
    'Ballard', 'Bander', 'Bar', 'Barbi', 'Barimah', 'Barnie', 'Barry', 'Bartley', 'Bashuk', 'Batha', 'Baudoin', 'Bayly',
    'Beasley', 'Beberg', 'Beeck', 'Behrens', 'Belayneh', 'Belle', 'Bendicta', 'Benil', 'Bennink', 'Berardo', 'Bergmann',
    'Berlauda', 'Bernelle', 'Berry', 'Bertolde', 'Bethel', 'Betty', 'Bevis', 'Bible', 'Bigod', 'Bilow', 'Birdie',
    'Bixby',
    'Blakelee', 'Blaseio', 'Blithe', 'Bluhm', 'Bobbette', 'Boehmer', 'Bohman', 'Bollen', 'Bonina', 'Booker', 'Borden',
    'Borreri', 'Boucher', 'Bowden', 'Boycie', 'Brackett', 'Braeunig', 'Brandie', 'Braunstein', 'Breen', 'Brenna',
    'Briana',
    'Brietta', 'Bringhurst', 'Brittany', 'Broder', 'Bronnie', 'Brott', 'Brunella', 'Bryner', 'Buckley', 'Buffy', 'Bum',
    'Burchett', 'Burkley', 'Burny', 'Busby', 'Butte', 'Byrom', 'Cadmarr', 'Caitrin', 'Calia', 'Calloway', 'Camel',
    'Campbell', 'Candyce', 'Caplan', 'Carbone', 'Cargian', 'Carlen', 'Carlstrom', 'Carmencita', 'Carolina', 'Carrick',
    'Cary', 'Casimire', 'Cassondra', 'Catha', 'Catima', 'Cavanagh', 'Ceciley', 'Celestyn', 'Centonze', 'Chace', 'Chak',
    'Chandless', 'Chapman', 'Charla', 'Charmion', 'Chavaree', 'Chema', 'Cherice', 'Chesney', 'Chickie', 'Chiou', 'Chon',
    'Christalle', 'Christis', 'Chu', 'Ciapha', 'Cinda', 'Cirone', 'Clarabelle', 'Clarisse', 'Claudio', 'Clein',
    'Cleodal',
    'Cliff', 'Close', 'Cnut', 'Codee', 'Cohe', 'Colburn', 'Collen', 'Colpin', 'Combe', 'Conchita', 'Conner', 'Constant',
    'Cooley', 'Corabelle', 'Cordie', 'Corin', 'Cornelie', 'Corrinne', 'Cosetta', 'Cottrell', 'Covell', 'Craggy',
    'Crean',
    'Cressler', 'Cristian', 'Crompton', 'Cruickshank', 'Culliton', 'Currey', 'Cutlip', 'Cynara', 'Cyril', 'Dael',
    'Dahlstrom', 'Dallis', 'Dambro', 'Danczyk', 'Daniell', 'Dante', 'Darby', 'Darice', 'Darrelle', 'Dasha', 'Davey',
    'Dawn',
    'Dearborn', 'Decato', 'Deedee', 'Dela', 'Delija', 'Delos', 'Deming', 'Denie', 'Denver', 'Dermot', 'Des', 'Deste',
    'Devland', 'Dewitt', 'Dianemarie', 'Dich', 'Dielle', 'Dimitri', 'Dinsmore', 'Dittman', 'Docile', 'Doi', 'Dolphin',
    'Dominus', 'Donela', 'Donny', 'Dorcus', 'Dorinda', 'Dorothi', 'Dosi', 'Douglas', 'Downs', 'Dream', 'Driskill',
    'Drummond', 'Dudden', 'Dulcia', 'Dunham', 'Durant', 'Durward', 'Duvall', 'Dyanne', 'Eachelle', 'Earley', 'Ebby',
    'Eckart', 'Edea', 'Edina', 'Edmonds', 'Edva', 'Egarton', 'Ehrlich', 'Eisenstark', 'Elberta', 'Eldreeda', 'Eleph',
    'Eliathan', 'Elish', 'Ellerd', 'Ellora', 'Elnore', 'Elsie', 'Elvis', 'Emalia', 'Emersen', 'Emmalee', 'Emmuela',
    'Eng',
    'Ennis', 'Ephrayim', 'Erastus', 'Erica', 'Erland', 'Ermine', 'Erroll', 'Esma', 'Estell', 'Ethan', 'Etoile',
    'Eugene',
    'Euphemie', 'Evander', 'Evelyn', 'Evslin', 'Ezana', 'Fabio', 'Fadil', 'Fairman', 'Fanchon', 'Fari', 'Farny',
    'Fasano',
    'Faus', 'Fawnia', 'Fedak', 'Feldt', 'Feliza', 'Fenner', 'Feriga', 'Ferrel', 'Fia', 'Fiertz', 'Fillander', 'Fini',
    'Firman', 'Fitzpatrick', 'Fleeman', 'Flip', 'Florin', 'Flss', 'Fonsie', 'Forras', 'Foskett', 'France', 'Francoise',
    'Franz', 'Freda', 'Fredette', 'French', 'Friedberg', 'Frodeen', 'Fruma', 'Fullerton', 'Fusco', 'Gabrielle', 'Gahan',
    'Galatia', 'Gamali', 'Garaway', 'Gare', 'Garlen', 'Garris', 'Gaspar', 'Gauldin', 'Gavrielle', 'Gayner', 'Gefen',
    'Gemina', 'Genisia', 'Geoffry', 'Georglana', 'Gerfen', 'Germana', 'Gerstner', 'Gherardi', 'Gibb', 'Giesser',
    'Gilberto',
    'Gill', 'Gilmore', 'Ginny', 'Girardi', 'Giuditta', 'Gladis', 'Glenda', 'Glover', 'Godber', 'Goer', 'Goldin',
    'Gomar',
    'Goodden', 'Gordie', 'Gotcher', 'Gow', 'Graham', 'Granny', 'Graybill', 'Greenstein', 'Gregory', 'Greyso',
    'Grimbald',
    'Groark', 'Grosvenor', 'Gualterio', 'Guild', 'Gunilla', 'Gusba', 'Guthrey', 'Gwenora', 'Hachmann', 'Haerle',
    'Haile',
    'Haldane', 'Hall', 'Halpern', 'Hamid', 'Hamrnand', 'Hankins', 'Hanser', 'Hardan', 'Harim', 'Harms', 'Harriette',
    'Hartmunn', 'Hasheem', 'Hatfield', 'Havener', 'Hayman', 'Hazen', 'Hebert', 'Hedvah', 'Heidie', 'Heise', 'Helenka',
    'Helsie', 'Hendry', 'Henricks', 'Hepsiba', 'Hermann', 'Herrah', 'Hertz', 'Hess', 'Hewie', 'Hidie', 'Hilary',
    'Hillegass', 'Hime', 'Hiroshi', 'Hoashis', 'Hoem', 'Hola', 'Hollinger', 'Holtorf', 'Honora', 'Horacio', 'Hortense',
    'Hound', 'Howlond', 'Huberman', 'Hufnagel', 'Hulen', 'Hun', 'Hurless', 'Hutchinson', 'Hyde', 'Iaria', 'Idel',
    'Ieso',
    'Ihab', 'Ilise', 'Imelda', 'Infeld', 'Ingold', 'Iny', 'Iphigeniah', 'Irmina', 'Isac', 'Isidora', 'Israel', 'Ive',
    'Iz',
    'Jacie', 'Jacoba', 'Jacquette', 'Jaffe', 'Jala', 'Jamison', 'Janelle', 'Janis', 'Janyte', 'Jariah', 'Jarvis',
    'Jaye',
    'Jeanna', 'Jeffcott', 'Jehovah', 'Jen', 'Jennee', 'Jerad', 'Jerol', 'Jesher', 'Jeth', 'Jillana', 'JoAnne', 'Jobe',
    'Jody', 'Johanan', 'Johns', 'Jolenta', 'Jones', 'Jordon', 'Joselow', 'Josselyn', 'Jozef', 'Judus', 'Julie', 'Juni',
    'Justine', 'Kaela', 'Kaitlynn', 'Kalin', 'Kama', 'Kania', 'Karas', 'Karissa', 'Karlyn', 'Kary', 'Kassity',
    'Katheryn',
    'Katonah', 'Kaufmann', 'Kaz', 'Keeler', 'Keiko', 'Kelila', 'Kelsy', 'Kendrah', 'Kenneth', 'Kenwee', 'Kerman',
    'Kery',
    'Kevin', 'Khichabia', 'Kieran', 'Killian', 'Kimmel', 'Kingston', 'Kira', 'Kirsteni', 'Kitty', 'Klement', 'Klos',
    'Knowle', 'Kobylak', 'Kolk', 'Konstantine', 'Korenblat', 'Kosel', 'Kowtko', 'Krause', 'Krenn', 'Kristel', 'Krock',
    'Krystalle', 'Kumler', 'Kusin', 'Kyla', 'LaMee', 'Lachman', 'Lahey', 'Lali', 'Lammond', 'Lancelot', 'Landry',
    'Langston', 'Laraine', 'Larkin', 'Lashondra', 'Latimer', 'Latt', 'Launcelot', 'Lauretta', 'Lavena', 'Lawson',
    'LeMay',
    'Leanora', 'Leclair', 'Leesen', 'Leid', 'Lela', 'Lemon', 'Lenno', 'Leon', 'Leontina', 'Leshia', 'Letizia',
    'Leveridge',
    'Lewellen', 'Lezlie', 'Libby', 'Lidia', 'Lila', 'Lily', 'Lindbom', 'Lindy', 'Linnie', 'Lipscomb', 'Liss', 'Liu',
    'Lizzy', 'Lodmilla', 'Lolande', 'Longan', 'Lopes', 'Lorena', 'Lorinda', 'Lorry', 'Lotus', 'Loux', 'Lowney',
    'Lubeck',
    'Lucic', 'Lucy', 'Luelle', 'Lulita', 'Lunneta', 'Lustick', 'Lyford', 'Lynelle', 'Lysander', 'MacGregor',
    'Maccarone',
    'Macy', 'Madelaine', 'Madonia', 'Magda', 'Magna', 'Mahon', 'Maire', 'Malamud', 'Malia', 'Mallis', 'Malvie', 'Mandi',
    'Manny', 'Manya', 'Marcellina', 'Marcoux', 'Margalo', 'Margit', 'Mariano', 'Marigolde', 'Marion', 'Market',
    'Marler',
    'Maro', 'Marrissa', 'Martelli', 'Martinson', 'Marya', 'Marysa', 'Mastic', 'Mathian', 'Matthaus', 'Maud', 'Maurili',
    'Maxentia', 'Mayce', 'Mazonson', 'McClelland', 'McCullough', 'McGraw', 'McKinney', 'McNeely', 'Meaghan', 'Medora',
    'Meghan', 'Mela', 'Melessa', 'Mella', 'Melody', 'Mendelsohn', 'Meraree', 'Meredi', 'Merlin', 'Merrill', 'Meta',
    'Micaela', 'Michelina', 'Middendorf', 'Mikael', 'Milburr', 'Millar', 'Milon', 'Miner', 'Minta', 'Mirilla',
    'Mitinger',
    'Modeste', 'Mohr', 'Molly', 'Monika', 'Monteith', 'Mord', 'Morganne', 'Morra', 'Mosa', 'Mossman', 'Moyna',
    'Mulcahy',
    'Munford', 'Murdock', 'Muslim', 'Myra', 'Naamana', 'Nadean', 'Nahshu', 'Names', 'Nanny', 'Nari', 'Natal',
    'Nathanial',
    'Nazar', 'Neddy', 'Neile', 'Nellir', 'Neri', 'Nessie', 'Neumark', 'Newby', 'Niall', 'Nicki', 'Nicolella',
    'Nightingale',
    'Nikos', 'Niobe', 'Noach', 'Noell', 'Nollie', 'Nord', 'Normi', 'Norvell', 'Nozicka', 'Nyhagen', 'Obau', 'Obrien',
    'Odele', 'Odom', 'Ogg', 'Olatha', 'Olga', 'Olly', 'Olympe', 'Ondine', 'Oona', 'Orbadiah', 'Orgell', 'Orlando',
    'Ornstead', 'Orthman', 'Osborn', 'Ossie', 'Othelia', 'Otto', 'Ozzie', "O'Meara", 'Packer', 'Paige', 'Palma',
    'Panayiotis', 'Paola', 'Pardoes', 'Parrish', 'Pascale', 'Patience', 'Patterman', 'Paulita', 'Paxton', 'Pearlman',
    'Pedroza', 'Pelaga', 'Pena', 'Pentha', 'Per', 'Perloff', 'Perseus', 'Peterson', 'Petronilla', 'Pfeifer', 'Phene',
    'Philine', 'Phillis', 'Phox', 'Piefer', 'Pike', 'Pinter', 'Piselli', 'Plante', 'Plumbo', 'Polito', 'Pomona',
    'Popelka',
    'Portwine', 'Power', 'Prendergast', 'Priebe', 'Prissie', 'Proudfoot', 'Pryor', 'Pulcheria', 'Puto', 'Queenie',
    'Quince',
    'Quiteris', 'Rachel', 'Radloff', 'Raffaello', 'Rahr', 'Rakia', 'Ramey', 'Randal', 'Ranit', 'Rapp', 'Ratib', 'Ray',
    'Rayshell', 'Rebbecca', 'Redfield', 'Reeva', 'Reiche', 'Reinhard', 'Rem', 'Rene', 'Renwick', 'Reuven', 'Rhea',
    'Rhodie',
    'Ribble', 'Richela', 'Ricker', 'Riegel', 'Riki', 'Rintoul', 'Ritchie', 'Roana', 'Robert', 'Robyn', 'Rockie',
    'Rodie',
    'Roer', 'Rolando', 'Romanas', 'Romonda', 'Ronny', 'Rosa', 'Rosanne', 'Rosemare', 'Rosenthal', 'Rossen', 'Rothwell',
    'Rowney', 'Roz', 'Ruberta', 'Rudin', 'Rufford', 'Ruperta', 'Russo', 'Ruthy', 'Saba', 'Sachi', 'Sadler', 'Saied',
    'Salas', 'Sallee', 'Salvador', 'Sami', 'Sanborne', 'Sandry', 'Santa', 'Sarajane', 'Sartin', 'Saum', 'Savior',
    'Saylor',
    'Schaeffer', 'Scheider', 'Schlesinger', 'Schoening', 'Schriever', 'Schwartz', 'Scotti', 'Seaden', 'Sebastiano',
    'Seem',
    'Seiter', 'Selhorst', 'Selmner', 'Seow', 'Sergius', 'Seto', 'Seymour', 'Shakti', 'Shanie', 'Shargel', 'Shaughnessy',
    'Shear', 'Shel', 'Shelton', 'Shere', 'Sherr', 'Sheya', 'Shippee', 'Shoifet', 'Shue', 'Shute', 'Sibley', 'Sidon',
    'Siesser', 'Sik', 'Silsby', 'Simah', 'Sinclair', 'Sirotek', 'Skantze', 'Skipton', 'Slayton', 'Smart', 'So',
    'Solberg',
    'Sommer', 'Sophey', 'Sosna', 'Spalla', 'Spence', 'Spohr', 'Stacey', 'Stan', 'Stanton', 'Staten', 'Steele',
    'Steinke',
    'Stephenie', 'Stevena', 'Stillas', 'Stoecker', 'Stouffer', 'Streetman', 'Stroup', 'Stutsman', 'Sugihara', 'Sunda',
    'Susana', 'Suzan', 'Swamy', 'Swetlana', 'Sybille', 'Synn', 'Tace', 'Taggart', 'Talbert', 'Tam', 'Tammie',
    'Tannenbaum',
    'Tarr', 'Tate', 'Tawney', 'Tedda', 'Tegan', 'Ten', 'Terbecki', 'Terrance', 'Tertia', 'Tews', 'Thanh', 'Thedrick',
    'Therese', 'Thibaut', 'Thomajan', 'Thorma', 'Three', 'Tibbitts', 'Tiertza')


def watermark_check(feed_img, image64):
    position = 0, 0
    is_normal = False
    base64_data = re.sub('^data:image/.+;base64,', '', image64)
    bin = base64.b64decode(base64_data)
    img_data = BytesIO(bin)
    img_cheker = Image.open(img_data)

    base64_feed = re.sub('^data:image/.+;base64,', '', feed_img)
    bin = base64.b64decode(base64_feed)
    img_data = BytesIO(bin)
    water_img = Image.open(img_data)
    watermark = Image.open('watermark.png').convert('RGBA')
    watermark.putalpha(128)
    width, height = img_cheker.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(img_cheker, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.putalpha(255)
    count = 0
    for y in range(300):
        for x in range(400):
            coord = x, y
            pixel_water = water_img.getpixel(coord)
            pixel_trans = transparent.getpixel(coord)
            if pixel_trans[0] == pixel_water[0] and pixel_trans[1] == pixel_water[1] and pixel_trans[2] == pixel_water[
                2]:
                count += 1
    if count == 120000:
        is_normal = True
    return is_normal


def lsb_decrupt(image64):
    base64_data = re.sub('^data:image/.+;base64,', '', image64)
    bin = base64.b64decode(base64_data)
    img_data = BytesIO(bin)
    img = Image.open(img_data)
    width, height = img.size
    flag_bin = ""
    flag = ""
    is_flag = False
    for y in range(height - 1):
        if is_flag:
            break
        for x in range(width - 1):
            if len(flag_bin) == 256:
                is_flag = True
                break
            coord = x, y
            pixel = img.getpixel(coord)
            this = "000" + "{0:b}".format(pixel[0])
            flag_bin += this[len(this) - 3:len(this) - 1]
            this = "000" + "{0:b}".format(pixel[1])
            flag_bin += this[len(this) - 3:len(this) - 1]
        if is_flag:
            break

    for i in range(0, len(flag_bin), 8):
        flag += chr(int(flag_bin[i:i + 8], 2))
    return flag


def fibi_decrypt(image64):
    base64_data = re.sub('^data:image/.+;base64,', '', image64)
    bin = base64.b64decode(base64_data)
    img_data = BytesIO(bin)
    img = Image.open(img_data)
    width, height = img.size
    a = 1
    b = 1
    flag = ""
    for i in range(11):
        x = b % width - 1
        y = b // width
        a, b = b, a
        b += a
        coord = x, y
        pixel = img.getpixel(coord)
        flag += chr(pixel[0] // 2)
        flag += chr(pixel[1] // 2)
        flag += chr(pixel[2] // 2)
        # print(flag)

    flag = flag[0:len(flag) - 1]
    flag = flag[::-1]
    return flag


def text_decrypt(image64):
    flag = ""
    base64_data = re.sub('^data:image/.+;base64,', '', image64)
    bin = base64.b64decode(base64_data)
    img_data = BytesIO(bin)
    img = Image.open(img_data)
    print(pytesseract.image_to_string(img))
    thresh = 200
    fn = lambda x: 255 if x > thresh else 0
    r = img.convert('L').point(fn, mode='1')
    text = pytesseract.image_to_string(r)
    for i in range(len(text)):
        flag += text[i]
    return flag


def get_random_name():
    """
    Генерация рандомного имени пользователя для регистрации
    """
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(10000, 99999))


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


# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def push(args: PushArgs) -> CheckerResult:
    try:  # try gen creds
        login = get_random_name()
        password = get_password()
        creds = {"Login": login, "Password": password}
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.ERROR.value} checker can not generate creds')

    res = CheckerResult(status=Status.OK.value,
                        private_info=json.dumps(creds),
                        public_info='PUSH works')
    headers = {'Content-Type': 'application/json', 'User-Agent': rnd_agent()}
    try:  # try registrate
        r = requests.post(f'http://{args.host}:{PORT}/backend/adduser',  # https://localhost:7180/api/User
                          json=json.loads(json.dumps(creds)),
                          allow_redirects=False,
                          headers=headers)  # cookies='158b36ec3ea4f5484054ad1fd21407333c874ef0fa4f0c8e34387efd5464a1e9500e2277b0367d71a273e5b46fa0869a'
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    try:  # try authenticate
        r = requests.post(f'http://{args.host}:{PORT}/backend/authentication',
                          json=json.loads(json.dumps(creds)),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    token = json.loads(r.content)['access_token']
    try:  # try validate
        r = requests.post(f'http://{args.host}:{PORT}/backend/validate',
                          json=json.loads(json.dumps({'token': token})),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    try:
        photo_ind = random.randint(0, len(os.listdir('Pico')))
        with open('Pico/'+(os.listdir('Pico')[photo_ind]), 'rb') as image_file:
            encodedPhoto = base64.b64encode(image_file.read()).decode()
        photo = encodedPhoto
        method = random.randint(0, 2)
        subscript = "id: " + str(random.randint(0, 15747) - 346)
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.ERROR.value} checker can take photo')
    try:  # try new_post
        r = requests.post(f'http://{args.host}:{PORT}/backend/post',
                          json=json.loads(json.dumps(
                              {'photo': photo, 'Owner': creds['Login'], 'method': method, 'sign': args.flag,
                               'subscript': subscript})),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    id_post = int(r.content)
    try:  # try take_feed
        r = requests.post(f'http://{args.host}:{PORT}/backend/feed',
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    try:  # try your_post
        r = requests.post(f'http://{args.host}:{PORT}/backend/yourpost',
                          json=json.loads(json.dumps({'id': id_post, 'owner': creds['Login'], 'token': token})),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    return CheckerResult(status=Status.OK.value, private_info=json.loads(
        json.dumps({'id_post': id_post, 'token': token, 'method': method, 'creds': creds})), public_info='PUSH works')


def pull(args: PullArgs) -> CheckerResult:
    creds = args.private_info['creds']
    headers = {'Content-Type': 'application/json', 'User-Agent': rnd_agent()}
    try:  # try authenticate
        r = requests.post(f'http://{args.host}:{PORT}/backend/authentication',
                          json=json.loads(json.dumps(creds)),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    token = json.loads(r.content)['access_token']
    try:  # try validate
        r = requests.post(f'http://{args.host}:{PORT}/backend/validate',
                          json=json.loads(json.dumps({'token': token})),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    try:  # try take_feed
        r = requests.post(f'http://{args.host}:{PORT}/backend/feed',
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    water_photo = ""  # photo with watermark
    for post in json.loads(r.content):
        if (post['id'] == args.private_info['id_post']):
            water_photo = post['photoForAll']
    try:  # try your_post
        r = requests.post(f'http://{args.host}:{PORT}/backend/yourpost',
                          json=json.loads(json.dumps(
                              {'id': args.private_info['id_post'], 'owner': creds['Login'], 'token': token})),
                          allow_redirects=False, verify=False, headers=headers)
        if r.status_code != 200:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.DOWN.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.DOWN.value} Can not connect')
    clean_photo = json.loads(r.content)['photoForAll']  # photo without watermark
    try:  # try check watermark
        is_ = watermark_check(water_photo, clean_photo)
        if not is_:
            return CheckerResult(status=Status.MUMBLE.value,
                                 private_info=f'{r.status_code}',
                                 public_info=f'PUSH {Status.MUMBLE.value} {r.url} - {r.status_code}')
    except Exception as e:
        return CheckerResult(status=Status.ERROR.value,
                             private_info=str(e),
                             public_info=f'PUSH {Status.ERROR.value} checker can not check watermark')
    if args.private_info['method'] == 0:
        try:
            flag = lsb_decrupt(clean_photo)
            if flag != args.flag:
                return CheckerResult(status=Status.CORRUPT.value,
                                     private_info=f'{r.status_code}',
                                     public_info=f'PUSH {Status.CORRUPT.value} Can not restore lsb flag')
        except Exception as e:
            return CheckerResult(status=Status.ERROR.value,
                                 private_info=str(e),
                                 public_info=f'PUSH {Status.ERROR.value} Can not restore lsb flag')
    elif args.private_info['method'] == 1:
        try:
            flag = fibi_decrypt(clean_photo)
            if flag != args.flag:
                return CheckerResult(status=Status.CORRUPT.value,
                                     private_info=f'{r.status_code}',
                                     public_info=f'PUSH {Status.CORRUPT.value} Can not restore flag fibonachi')
        except Exception as e:
            return CheckerResult(status=Status.ERROR.value,
                                 private_info=str(e),
                                 public_info=f'PUSH {Status.ERROR.value} Can not restore flag fibonachi')

    elif args.private_info['method'] == 2:
        flag = text_decrypt(clean_photo)
        try:
            flag = text_decrypt(clean_photo)
            if flag != args.flag:
                return CheckerResult(status=Status.CORRUPT.value,
                                     private_info=f'{r.status_code}',
                                     public_info=f'PUSH {Status.CORRUPT.value} Can not restore flag text')
        except Exception as e:
            return CheckerResult(status=Status.ERROR.value,
                                 private_info=str(e),
                                 public_info=f'PUSH {Status.ERROR.value} Can not restore flag text')

    return CheckerResult(status=Status.OK.value, private_info=str(args.private_info), public_info='PULL works')


def readfile(path):
    with open(path, "r", encoding="utf-8") as file:  # заменить file_name на имя файла
        txt = file.read()
        txt = re.sub(r"\s", "", txt)
        out_txt = re.split(r"[()]", txt)
        return out_txt[0]


if __name__ == '__main__':
    import sys

    # action, *args = sys.argv[1:]
    action, *args = 'push', '127.0.0.1', 1, 'flag'
    #action, *args = 'pull', '127.0.0.1', {'id_post': 9,
                                          #'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiU3liaWxsZTQ1NTA2IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiVXNlciIsIm5iZiI6MTY4MTQ1NDEzOCwiZXhwIjoxNjgxNDU1MDM4LCJpc3MiOiJNeUF1dGhTZXJ2ZXIiLCJhdWQiOiJWdWxub2dyYW1tQ2xpZW50In0.PliY-ceFTiWAQaLK0w4COssQKqMv3w8qYUv0CtNULaM',
                                         # 'method': 1, 'creds': {'Login': 'Sybille45506',
                                                               #  'Password': 'ftrlzm)kfavUPmneL**R'}}, 'flag'
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
