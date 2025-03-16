#!/bin/bash

# Конфигурация
domain_ru="api.выручаемкаждыйдень.рф"
domain="api.xn--80aaekaddf2agvt2a6b8c3ckw.xn--p1ai"
email="your-email@example.com"    # Замените на свой email
staging=1                         # Установите в 0 для боевого сертификата
rsa_key_size=4096

# Проверка root прав
if [ "$EUID" -ne 0 ]; then 
    echo "Запустите скрипт с правами root"
    exit 1
fi

# Создаем необходимые директории
echo "Создаем директории для certbot..."
mkdir -p certbot/conf/live/$domain_ru
mkdir -p certbot/www

# Создаем временный самоподписанный сертификат
echo "Создаем временный сертификат..."
openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \
    -keyout certbot/conf/live/$domain_ru/privkey.pem \
    -out certbot/conf/live/$domain_ru/fullchain.pem \
    -subj '/CN=localhost'

# Остановка существующих контейнеров
echo "Останавливаем контейнеры..."
docker-compose -f docker-compose.prod.yml down

echo "Запускаем nginx..."
docker-compose -f docker-compose.prod.yml up -d nginx
echo "Ждем запуск nginx..."
sleep 5

# Удаляем временный сертификат
echo "Удаляем временный сертификат..."
rm -rf certbot/conf/live/$domain_ru/*

# Запрашиваем сертификат
echo "Запрашиваем сертификат Let's Encrypt..."
if [ $staging != "0" ]; then
    staging_arg="--staging"
else
    staging_arg=""
fi

# Проверяем доступность домена
echo "Проверяем доступность домена..."
curl -I http://$domain_ru

echo "Запускаем certbot..."
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "\
    certbot certonly --webroot \
    -w /var/www/certbot \
    $staging_arg \
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

echo "Проверяем статус сертификата..."
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

echo "Готово! Проверьте работу сайта по адресу https://$domain_ru"
echo "Если вы использовали staging=1, то браузер покажет предупреждение о сертификате"
echo "Для получения боевого сертификата установите staging=0 и запустите скрипт снова" 