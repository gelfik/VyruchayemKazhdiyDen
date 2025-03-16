# Выручаем Каждый День API

Проект на Django для управления донатами и пожертвованиями.

## Технологии

- Python 3.11
- Django 5.2
- PostgreSQL 15
- Docker & Docker Compose
- Nginx
- Gunicorn
- Django REST Framework

## Требования

- Docker
- Docker Compose
- Git

## Структура проекта

```
VyruchayemKazhdiyDen/
├── core/                    # Основной модуль Django
├── donation/               # Приложение для управления донатами
├── templates/              # HTML шаблоны
├── static/                 # Статические файлы
├── media/                  # Медиа файлы
├── docker-compose.dev.yml  # Конфигурация Docker для разработки
├── docker-compose.prod.yml # Конфигурация Docker для продакшена
├── Dockerfile.dev          # Dockerfile для разработки
├── Dockerfile.prod         # Dockerfile для продакшена
├── nginx/                  # Конфигурация Nginx
├── requirements.txt        # Зависимости Python
└── .env.template          # Шаблон переменных окружения
```

## Установка и запуск

### Разработка (Dev окружение)

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd VyruchayemKazhdiyDen
```

2. Создайте файл `.env`:
```bash
cp .env.template .env
```

3. Запустите проект:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

4. В отдельном терминале выполните базовую настройку:
```bash
# Миграции
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Создание суперпользователя
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input
```

Приложение будет доступно по адресу: http://localhost:8000

## Развертывание в продакшн окружении

### Предварительные требования

1. Установленный Docker и Docker Compose
2. Зарегистрированный домен (api.выручаемкаждыйдень.рф)
3. Открытые порты 80 и 443 на сервере

### Шаги развертывания

1. Клонируйте и настройте проект:
```bash
git clone <repository-url>
cd VyruchayemKazhdiyDen
cp .env.template .env
```

2. Настройте `.env` файл:
```
POSTGRES_DB=vyruchayem_db
POSTGRES_USER=<ваш-пользователь>
POSTGRES_PASSWORD=<ваш-пароль>
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=<ваш-секретный-ключ>
DEBUG=0
```

3. Настройте SSL:
```bash
# Создайте директории для сертификатов
mkdir -p certbot/conf certbot/www

# Настройте email в скрипте
nano init-letsencrypt.sh

# Получите сертификат
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

4. Запустите приложение:
```bash
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

### Особенности конфигурации

#### Dev окружение
- Django runserver с включенным режимом отладки
- Монтирование локальных файлов для удобства разработки
- Отдельные тома для разработки

#### Prod окружение
- Gunicorn с отключенным режимом отладки
- Многоэтапная сборка Docker
- Nginx как прокси-сервер с SSL
- Настроенные healthcheck для всех сервисов
- Кэширование статических файлов через Whitenoise

### Обслуживание

#### Мониторинг
```bash
# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Логи
docker-compose -f docker-compose.prod.yml logs -f [сервис]

# Использование ресурсов
docker stats $(docker-compose -f docker-compose.prod.yml ps -q)
```

#### SSL-сертификат
```bash
# Проверка статуса
docker-compose -f docker-compose.prod.yml exec certbot certbot certificates

# Обновление сертификата (автоматическое каждые 90 дней)
./init-letsencrypt.sh
```

#### Резервное копирование
```bash
# База данных
docker-compose -f docker-compose.prod.yml exec db pg_dump -U <пользователь> vyruchayem_db > backup_$(date +%Y%m%d).sql

# Медиафайлы
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

#### Обновление приложения
```bash
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### Безопасность

1. Все секретные данные хранятся в `.env`
2. Регулярное обновление Docker образов
3. Настроенный файрвол
4. Регулярные бэкапы
5. HTTPS с автообновлением сертификатов
6. Непривилегированный пользователь в контейнерах

### Устранение неполадок

При проблемах проверьте:
1. Статус контейнеров и их логи
2. Настройки SSL и сертификаты
3. Доступность базы данных
4. Права доступа к файлам
5. Сетевые подключения и порты

## Лицензия

MIT 