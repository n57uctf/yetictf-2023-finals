"""
This module:
    - create database tables
    - collect static files
    - create admin
    - fill database
"""
import os

if os.path.exists('inithialized'):
    os.system('gunicorn store.wsgi:application -b 0.0.0.0:8000 --reload')
    exit(0)

import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()
from products.models import Products
from promocodes.models import PromoCodes

os.system('python3 manage.py collectstatic --noinput')
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')

try:
    User = get_user_model()
    User.objects.create_superuser(username='admin', password='admin')
except:
    ...

_promo_codes = {
    'af3868c2311eed4d20917eb2c0195ae5c4c7415e8cc4b967429ff234dea3645f': 100,
    'ce403f504d4bf7be59fe271a75633b3bfba04fe43aca622a63e2f6dc67e0dec9': 100,
    '6774b0a45f74ccc917e7bbea65b9cdd70053ec1cc4b3b5734724bd247814ab80': 1500,
    '97aca45ca93483d21a955e57c4cd240e485c3bb6231be3a486c4bfa340209943': 3000,
    'f137036a6829f669c46ef2e119663af67150a2903171cb4279b73cde5e270b74': 1000,
    '49bf034118021ffc45f69a0248d31d3259d84ea03323ca65e0d69e164fdadffb': 1000,
    '7d68441ae7e44f644cf9738fed11369e653d024ac27f57879335dfb4aa6828cb': 2500,
    '05d066dcc272ee829ebba7cd2b390a84c6b5a98157a1bd73e1f337d3fc761be8': 1700,
    '0482f6eefc0ec185cc0c78c831d21650f85ebfaa6503dd9677c25cbfe5b041f8': 100
}

test_code = PromoCodes.objects.filter(code='af3868c2311eed4d20917eb2c0195ae5c4c7415e8cc4b967429ff234dea3645f').first()
if test_code is None:
    for code, amount in _promo_codes.items():
        PromoCodes.objects.create(code=code, amount=amount)

_products = {
    'Compact refrigerator': {
        'description': 'Refrigeratorin a white case is an ideal model for giving, office or hotel room. The volume of the refrigerating chamber of the presented model is 43 liters. It is divided into 2 large metal shelves and a small freezer drawer. In the balconies of the door you can store juices, cheeses, long-term storage dairy products in sealed packages.',
        'price': 5000
    },
    'Electric kettle': {
        'description': 'The electric kettle in a silver case will become your indispensable companion, allowing you to boil a large amount of water in a matter of minutes. The internal volume of the device is 1.8 liters, and its power is 1500 watts. The closed heating element made of steel contributes to the durability of the device and its attractive appearance. It also provides rapid heating of water in the tank. The entire body of the kettle is also made of steel, making it easy to clean.',
        'price': 12_000
    },
    'Vacuum cleaner': {
        'description': 'With the vacuum cleaner, you will arrange a real cleaning "storm" at home, and it will not be difficult to maintain daily cleanliness with it. The lightweight body is comfortable to carry in your hands from place to place, and the 4.5 m long rein makes it possible to get out at a considerable distance from the outlet. All collected contaminants are sent to a 0.8 liter container. Thanks to the HEPA filter, they have no chance to "get out" of there and get back into the air. To collect wool, the device has a special turbo brush.',
        'price': 8000
    },
    'Washing machine': {
        'description': 'The washing machine is notable for its laconic design and popular functionality. This model provides for loading a maximum of 6 kg of laundry and 23 automatic programs for performing various tasks. The control panel contains buttons with indicators and symbols, as well as a rotary control. It is equipped with a delay start timer up to 9 hours and an audible alarm with the ability to turn off. The auto-balance system distributes clothes in the drum for efficient and gentle spinning.',
        'price': 20_000
    },
    'Suspended extractor hood': {
        'description': 'Suspended hood in a white casing is made of metal with stainless steel edging, which makes it a reliable and durable appliance, without which no kitchen is imagined. It uses the "Removal" and "Circulation" modes, guaranteeing the effective removal of air polluted by aromas and fumes, as well as its replacement with fresh air. Thanks to this, you will feel comfortable being in the kitchen.',
        'price': 50_000
    },
    '6.7" Smartphone Pro Max': {
        'description': 'Smartphone Pro Max 1000 gigabytes presented in purple. It has the function of slow motion in FullHD, and can also shoot 4K video. There are three cameras on the back of the smartphone, one of which is 48MP and the other two are 12MP. The front camera is also 12 MP.',
        'price': 15_000
    },
    '5" Smartphone ': {
        'description': 'The smartphone is a simple and convenient device for calls, communication, surfing the Internet and viewing photo and video files. The turquoise model is made of durable plastic, and the installation of two SIM-cards makes it easier to choose a tariff and save on communication. The 5-inch IPS screen provides high quality pictures. A 4-core processor and 1 GB of RAM provide optimal performance.',
        'price': 4000
    },
    '13.3" Laptop': {
        'description': 'The laptop a stylish corporate design, compact size and high performance. Lightweight mobile computer in an aluminum case will become a reliable assistant for working with office editors, searching for information on the Internet and performing other everyday tasks. It has integrated graphics accelerator, 8 GB of RAM and 256 GB SSD storage, the system is fast. The laptop is running macOS.',
        'price': 35_000
    },
    '16.2" Laptop': {
        'description': 'The super-fast Laptop deliver phenomenal performance and surprisingly long battery life. Add to that a stunning Liquid Retina XDR display and even more ports for professional work. This is the laptop youve been waiting for.',
        'price': 17500
    },
    '15.6" Notebook': {
        'description': 'The laptop is designed for those who want to get a high-quality and productive computer device with the most requested functionality. This model fully satisfies these requirements. Reliable storage gives you long-term storage options for the virtual information you need. The device is equipped with a webcam and microphone, thanks to which you can organize video conferences with business partners and work colleagues.',
        'price': 60_000
    },
    '88" TV': {
        'description': 'You are not just watching TV, real life is unfolding before your eyes. The TV combines the deep rich colors of an OLED display with self-illuminating pixels and the enormity of 8K resolution. Self-illuminating pixels achieve the deepest blacks for crisp contrast in any light. Visual images are sharper, so you can make out subtle details that are usually invisible to the eye. The all-new Dynamic Tone Mapping Pro technology improves image quality. Previously, only the contours were improved. The technology now focuses on 5,000 blocks across the entire screen for brighter HDR down to the smallest detail.',
        'price': 10_000
    },
    'Video card': {
        'description': 'Here is a revolutionary low-profile graphics card. Since the model boasts a compact design (the length of the PC component is 14.6 cm and the width is only 6.9 cm), it will be an excellent purchase for a thin body. When connecting the model to the motherboard, it will need to occupy two expansion slots. To connect the model to the motherboard, a PCI-E version 2.0 connection interface is provided.',
        'price': 10_000
    },
    'Laser printer': {
        'description': 'The laser printer will be an excellent choice for home and office use. With it, you can easily create a large amount of paper documentation in a short period of time. The printer is based on black and white laser technology, which is distinguished by its efficiency and quality.',
        'price': 10_000
    },
    'Scanner': {
        'description': 'The scanner is presented in an elegant thin design, weighs 4.3 kg and measures 58.9x40.7x6.8 cm. The flatbed design with a durable glass substrate allows you to work with both single sheets and thick books.',
        'price': 14_000
    },
    'Screen for projector': {
        'description': '67" Projector screen is a high-quality equipment that is made of proven materials. When creating it, the manufacturer took into account every nuance. Thanks to this, it was possible to achieve excellent screen performance. It is adapted for installation in various rooms - in classrooms and auditoriums, in conference halls, offices, etc.',
        'price': 13_750
    },
    'Wi-Fi роутер': {
        'description': 'Wi-Fi-роутер в компактном корпусе черного цвета отличается повышенной функциональностью: он выполняет функции и маршрутизатора, и точки доступа, и репитера.',
        'price': 45_000
    },
    'LAN card': {
        'description': 'A network card will be required for users of stationary or mobile computers that are not equipped with a network adapter. The model is a compact white device that connects to a USB port. The network card is characterized by a maximum data transfer rate of 100 Mbps.',
        'price': 3000
    },
    'Switch': {
        'description': 'The 5-port switch is suitable for use as part of a corporate or home network. The device supports data transfer rates up to 1 Gbps. The switch is of the unmanaged type.',
        'price': 5000
    },
    'Chainsaw': {
        'description': 'The chainsaw is made in an ergonomic body weighing 6.9 kg and has a balanced design. This makes it easy to work with the tool, use it for felling small trees, chopping firewood, sawing boards, and also for cutting branches. The tool is based on a 2300 W gasoline engine, which corresponds to 3.1 hp. Its working volume is 45 cm³.',
        'price': 12_000
    },
    'Hair dryer': {
        'description': 'The hair dryer is presented in a full-size purple case with a 1.5 m cable and a comfortable folding handle. The design is also complemented by a small loop that allows you to store the device suspended. Delivery is carried out together with a concentrator nozzle with a landing diameter of 4.5 cm.',
        'price': 13_500
    },
    'Trimmer': {
        'description': 'The trimmer is designed for trimming nose and ear hair. Runs on one AA battery.',
        'price': 15_000
    },
    'Grill': {
        'description': 'An electric grill press with a maximum power of 1800 watts will help you cook meat, fish or vegetables with a golden crust at home at any time of the year. The fixation of the opening of the plates measuring 250x152 mm at 105 ° contributes to the special comfort in using the device: it is convenient to put the products into the grill press and then take them out. The maximum heating temperature is 190°.',
        'price': 8_000
    },
    'Built-in washing machine': {
        'description': 'The built-in washing machine is of the full-size type - its drum can hold up to 9 kilograms of dry laundry, there is an auto-weighing function. The spin speed of the model reaches 1600 rpm. The washing machine is equipped with an ergonomic and durable inverter motor. It has a 12 year warranty.',
        'price': 5_000
    },
    'Combined hob': {
        'description': 'The black combo hob B with induction hobs is functional enough to comfortably cook a variety of dishes. 4 burners differ in their sizes from each other (120, 145, 160, 180, 200 mm), which will allow you to use dishes of different sizes for cooking. One of the burners has two circuits.',
        'price': 4_000
    },
    'Wall air conditioner': {
        'description': 'A split system will be an excellent choice for creating comfortable conditions in a residential area. This model uses at its core a productive and reliable compressor, as well as a safe and efficient refrigerant, thanks to which efficient cooling is possible.',
        'price': 5_000
    },
    'Water bottle': {
        'description': 'Stainless steel water bottle with a capacity of 750 ml, suitable for outdoor activities and everyday use.',
        'price': 4500
    },
    'Wireless earphones': {
        'description': 'Wireless earphones with noise cancelling and touch control features for a superior audio experience.',
        'price': 9000
    },
    'Smartwatch': {
        'description': 'Fitness tracker smartwatch with a heart rate monitor, sleep tracker, and water resistance for outdoor activities.',
        'price': 18000
    },
    'Electric toothbrush': {
        'description': 'Electric toothbrush with multiple brushing modes and a timer for effective dental care.',
        'price': 5500
    },
    'Induction cooktop': {
        'description': 'Portable induction cooktop with multiple temperature settings and a timer for quick and efficient cooking.',
        'price': 13000
    },
    'Fitness ball': {
        'description': 'Anti-burst exercise ball with a diameter of 65 cm, ideal for yoga, pilates, and home workouts.',
        'price': 5500
    },
    'Portable charger': {
        'description': 'Portable charger with a capacity of 10000 mAh and multiple USB ports for charging multiple devices at once.',
        'price': 7500
    },
    'Reusable shopping bags': {
        'description': 'Eco-friendly reusable shopping bags made of durable materials and available in various designs.',
        'price': 3000
    },
    'Food processor': {
        'description': 'Multi-purpose food processor with multiple attachments for chopping, slicing, and shredding.',
        'price': 22000
    },
    'Slow cooker': {
        'description': 'Slow cooker with multiple temperature settings and a timer for cooking healthy and delicious meals.',
        'price': 9000
    },
    'Air fryer': {
        'description': 'Air fryer with a capacity of 3.5 liters and multiple temperature settings for cooking healthy and crispy fried food.',
        'price': 14000
    },
    'Portable Bluetooth speaker': {
        'description': 'Portable Bluetooth speaker with a 10-hour battery life and a water-resistant design for outdoor use.',
        'price': 6500
    },
    'Electric razor': {
        'description': 'Electric razor with multiple cutting blades and a rechargeable battery for a smooth and close shave.',
        'price': 11000
    },
    'Resistance bands': {
        'description': 'Set of 5 resistance bands with varying levels of resistance, ideal for strength training and home workouts.',
        'price': 4000
    },
    'Collapsible umbrella': {
        'description': 'Collapsible umbrella with a compact design and a water-resistant canopy for protection from the rain.',
        'price': 3500
    },
    'Electric griddle': {
        'description': 'Electric griddle with a non-stick surface and adjustable temperature control for cooking pancakes, eggs, and more.',
        'price': 8500
    },
    'Immersion blender': {
        'description': 'Immersion blender with multiple speed settings and a detachable shaft for easy cleaning.',
        'price': 7500
    },
    'Smart bike lock': {
        'description': 'A bike lock that can be unlocked with a smartphone app and features anti-theft and location tracking capabilities.',
        'price': 7500
    },
    'Portable blender': {
        'description': 'A small and lightweight blender that can be used to make smoothies, shakes, and other drinks on the go.',
        'price': 4000
    },
    'Self-cleaning litter box': {
        'description': 'A litter box that automatically cleans itself and disposes of waste, reducing the need for manual cleaning.',
        'price': 12000
    },
    'Adjustable laptop stand': {
        'description': 'A stand that can be adjusted to different heights and angles, allowing for more comfortable and ergonomic laptop use.',
        'price': 5000
    },
    'Noise-cancelling headphones': {
        'description': 'Headphones that use advanced technology to cancel out background noise and provide a more immersive listening experience.',
        'price': 15000
    },
    'Smart water bottle': {
        'description': 'A water bottle that tracks water intake, reminds you to drink, and syncs with fitness apps.',
        'price': 3500
    },
    'Wireless charging pad': {
        'description': 'A charging pad that allows you to charge compatible devices without the need for cables or cords.',
        'price': 4500
    },
    'Air purifier': {
        'description': 'A device that removes pollutants and allergens from the air, improving indoor air quality.',
        'price': 20000
    },
    'Bluetooth meat thermometer': {
        'description': 'A meat thermometer that connects to your phone via Bluetooth, allowing you to monitor cooking temperature remotely.',
        'price': 5500
    },
    'Smart toothbrush': {
        'description': 'A toothbrush that uses sensors and AI to provide real-time feedback on brushing technique and dental hygiene.',
        'price': 9000
    },
    'LED Strip Lights': {
        'description': 'These lights are perfect for adding some ambiance to any room. With a remote control and multiple color options, you can create the perfect atmosphere for any occasion.',
        'price': 3500
    },
    'Wireless Earbuds': {
        'description': 'Enjoy your music without the hassle of wires. With Bluetooth connectivity and long battery life, these earbuds are perfect for your daily commute or workout.',
        'price': 5500
    },
    'Waterproof Bluetooth Speaker': {
        'description': 'Take your music anywhere with this waterproof speaker. With Bluetooth connectivity and a long battery life, you can enjoy your favorite tunes no matter where you are.',
        'price': 9700
    },
    'Adjustable Dumbbells': {
        'description': 'Get the perfect workout with these adjustable dumbbells. With weight ranges from 5 to 52.5 pounds, you can customize your workout to your specific needs.',
        'price': 17800
    },
    'Mini Food Processor': {
        'description': 'Chop, grind, and mix your favorite ingredients with this mini food processor. With a compact design and powerful motor, you can create delicious meals with ease.',
        'price': 4800
    },
    'Cordless Handheld Vacuum': {
        'description': 'Clean up messes quickly and easily with this cordless handheld vacuum. With a powerful motor and long battery life, you can clean up any mess in seconds.',
        'price': 9200
    },
    'Electric Toothbrush': {
        'description': 'Get a brighter, healthier smile with this electric toothbrush. With multiple brush heads and cleaning modes, you can customize your brushing experience for maximum results.',
        'price': 6100
    },
    'Portable Blender': {
        'description': 'Make your favorite smoothies and shakes on-the-go with this portable blender. With a powerful motor and rechargeable battery, you can create delicious drinks no matter where you are.',
        'price': 6800
    },
    'Smart Thermostat': {
        'description': 'Control the temperature of your home from anywhere with this smart thermostat. With WiFi connectivity and a user-friendly app, you can easily adjust the temperature to your liking.',
        'price': 15600
    },
    'Electric Wine Opener': {
        'description': 'Open your favorite bottle of wine with ease with this electric wine opener. With a sleek design and rechargeable battery, you can impress your guests with your wine-opening skills.',
        'price': 5900
    },
    'Indoor Plant Grow Light': {
        'description': 'Grow your favorite plants indoors with this plant grow light. With adjustable brightness and a timer function, you can create the perfect growing environment for your plants.',
        'price': 9400
    },
    'Wireless Charger': {
        'description': 'Charge your phone wirelessly with this Qi-compatible wireless charger. With a sleek design and fast charging capabilities, you can keep your phone powered up all day long.',
        'price': 4200
    },
}

products_django_objects = [
    Products(name=product_name, description=product_info.get('description'), price=product_info.get('price'))
    for product_name, product_info in _products.items()
]

Products.objects.bulk_create(products_django_objects)

os.system('touch inithialized')
os.system('gunicorn store.wsgi:application -b 0.0.0.0:8000 --reload')

