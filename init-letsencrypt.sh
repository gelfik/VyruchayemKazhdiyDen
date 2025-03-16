#!/bin/bash

domain="api.xn--80aafkpbcdcb3agfghez2axe1c.xn--p1ai"
email="your-email@example.com"  # Замените на свой email

# Остановим контейнеры если они запущены
docker-compose -f docker-compose.prod.yml down

# Создаем необходимые директории
mkdir -p certbot/conf certbot/www

# Запускаем nginx
docker-compose -f docker-compose.prod.yml up -d nginx

# Ждем запуска nginx
echo "Waiting for nginx to start..."
sleep 10

# Запрашиваем сертификат в режиме staging (тестовый режим)
docker-compose -f docker-compose.prod.yml run --rm certbot certbot certonly \
    --webroot \
    --webroot-path /var/www/certbot \
    --email $email \
    --agree-tos \
    --no-eff-email \
    --staging \
    -d $domain

# Если тестовый сертификат получен успешно, запрашиваем боевой
echo "Requesting production certificate..."
docker-compose -f docker-compose.prod.yml run --rm certbot certbot certonly \
    --webroot \
    --webroot-path /var/www/certbot \
    --email $email \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d $domain

# Перезапускаем nginx для применения сертификата
docker-compose -f docker-compose.prod.yml restart nginx 