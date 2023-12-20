FROM php:8.2-fpm
 
WORKDIR /var/www/html/data-visualization
 
COPY . .

RUN apt-get update && \
    apt-get install -y \
    libpng-dev \
    libpq-dev \
    zip \
    vim \
    git \
    curl

RUN docker-php-ext-install pdo pdo_mysql

RUN docker-php-ext-install pdo pdo_pgsql

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

USER root:www-data

EXPOSE 9000
ENTRYPOINT ["sh", "entry.sh"]