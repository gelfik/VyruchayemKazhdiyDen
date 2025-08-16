#!/bin/bash

# Конфигурация
domain="api.xn--90aahfa2cdbrfho3oc.xn--p1ai"
email="your-email@example.com"    # Замените на свой email
rsa_key_size=4096

# Проверка root прав
if [ "$EUID" -ne 0 ]; then 
    echo "Запустите скрипт с правами root"
    exit 1
fi

# Создаем необходимые директории
echo "Создаем директории для certbot..."
mkdir -p certbot/conf/live/$domain
mkdir -p certbot/www

# Останавливаем существующие контейнеры
echo "Останавливаем контейнеры..."
docker-compose -f docker-compose.prod.yml down

echo "Запускаем только nginx..."
docker-compose -f docker-compose.prod.yml up -d nginx
echo "Ждем запуск nginx..."
sleep 10

# Проверяем доступность домена
echo "Проверяем доступность домена..."
curl -I http://$domain

echo "Запускаем certbot..."
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "\
    certbot certonly --webroot \
    -w /var/www/certbot \
    --email $email \
    -d $domain \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal \
    --no-eff-email" certbot

# Перезапускаем все сервисы
echo "Перезапускаем все сервисы..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

echo "Проверяем статус nginx..."
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

echo "Готово! Проверьте работу сайта по адресу https://$domain" 