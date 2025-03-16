#!/bin/bash

domain="api.xn--80aafkpbcdcb3agfghez2axe1c.xn--p1ai"
email="your-email@example.com"  # Замените на свой email

# Создаем необходимые директории
mkdir -p "./certbot/conf/live/$domain"
mkdir -p "./certbot/www"

# Запускаем nginx
docker-compose -f docker-compose.prod.yml up --force-recreate -d nginx

# Запрашиваем сертификат
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --email $email \
    -d $domain \
    --rsa-key-size 4096 \
    --agree-tos \
    --force-renewal \
    --cert-name $domain" certbot

# Перезапускаем nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload 