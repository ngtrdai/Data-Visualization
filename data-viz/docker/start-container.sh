#!/usr/bin/env bash

if [ ! -z "$WWWUSER" ]; then
    usermod -u $WWWUSER dataviz
fi

cd /var/www/html/data-viz

chgrp -R www-data storage
chmod -R 770 storage

cp .env.example .env

if [ -f .env ]; then
    ENVIRONMENT=$(grep -E '^APP_ENV=' .env | cut -d '=' -f2)
    if [ "$ENVIRONMENT" = "local" ]; then
        echo "Running composer install..."
        composer install
        echo "Composer install completed."
    else
        echo "Environment is not local. Skipping composer install."
    fi
else
    echo "No .env file found. Aborting."
fi

while ! php artisan migrate --force; do
    echo "waiting for database ready"
done

composer dump-autoload
php artisan key:generate
php artisan cache:clear
php artisan optimize

if [ $# -gt 0 ]; then
    exec gosu $WWWUSER "$@"
else
    exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
fi
