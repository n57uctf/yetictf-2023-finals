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


Products.objects.create(name='Product 1', description='Description for product 1', price=3000)
Products.objects.create(name='Product 2', description='Description for product 2', price=5000)
Products.objects.create(name='Product 3', description='Description for product 3', price=10_000)


PromoCodes.objects.create(code='promo1', amount=500)
PromoCodes.objects.create(code='promo2', amount=1000)


os.system('touch inithialized')
os.system('gunicorn store.wsgi:application -b 0.0.0.0:8000 --reload')




