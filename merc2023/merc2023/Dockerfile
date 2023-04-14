FROM php:8.1-apache

RUN apt-get update && apt install -y libpq-dev libpng-dev libjpeg-dev libfreetype6-dev glibc-source

RUN docker-php-ext-configure gd --with-freetype --with-jpeg

RUN docker-php-ext-install -j10 gd

RUN docker-php-ext-install -j10 pgsql &&\
    docker-php-ext-install -j10 pdo_pgsql

ARG DB_PASSWORD

ENV DB_PASSWORD=${DB_PASSWORD}

RUN a2enmod rewrite
ADD ./source /var/www/html

RUN useradd -ms /bin/bash merc
RUN chown -R merc:merc /var/www/html
RUN chmod -R 777 /var/www/html
RUN service apache2 restart
RUN chown -R merc:merc /var/run/apache2 

USER merc
