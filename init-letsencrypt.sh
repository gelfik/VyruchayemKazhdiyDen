#!/bin/bash

domain="api.xn--80aafkpbcdcb3agfghez2axe1c.xn--p1ai"
email="your-email@example.com"  # Замените на свой email

# Остановим контейнеры если они запущены
docker-compose -f docker-compose.prod.yml down

# Создаем необходимые директории
mkdir -p certbot/conf certbot/www

# Запускаем только nginx
docker-compose -f docker-compose.prod.yml up -d nginx

# Ждем запуска nginx
echo "Waiting for nginx to start..."
sleep 10

echo "Requesting staging certificate..."
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --staging \
    --email $email \
    --rsa-key-size 4096 \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d $domain" certbot

echo "Requesting production certificate..."
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --email $email \
    --rsa-key-size 4096 \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d $domain" certbot

echo "Stopping nginx..."
docker-compose -f docker-compose.prod.yml stop nginx

echo "Starting all services..."
docker-compose -f docker-compose.prod.yml up -d 