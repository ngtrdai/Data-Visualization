FROM php:8.2-fpm-bullseye
ENV COMPOSER_ALLOW_SUPERUSER=1

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

RUN install-php-extensions xdebug-3.2.0

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

ENV APP_ENV=local
ENV APP_DEBUG=true
ENV APP_URL=http://localhost

USER root:www-data

EXPOSE 9000

ENTRYPOINT ["sh", "entry.sh"]