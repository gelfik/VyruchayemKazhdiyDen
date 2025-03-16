# Vyruchayem Kazhdiy Den

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

## Установка и запуск

### Разработка (Dev окружение)

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd VyruchayemKazhdiyDen
```

2. Создайте файл `.env` из шаблона:
```bash
cp .env.template .env
```

3. Запустите проект:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

4. В отдельном терминале выполните миграции:
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
```

5. Создайте суперпользователя:
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

6. Соберите статические файлы:
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --no-input
```

Приложение будет доступно по адресу: http://localhost:8000

### Продакшен (Prod окружение)

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd VyruchayemKazhdiyDen
```

2. Создайте файл `.env` из шаблона и настройте переменные окружения:
```bash
cp .env.template .env
# Отредактируйте .env файл, установив безопасные значения
```

3. Запустите проект:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

4. Выполните миграции:
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

5. Создайте суперпользователя:
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

6. Соберите статические файлы:
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

Приложение будет доступно по адресу: http://localhost

## Полезные команды

### Dev окружение
```bash
# Просмотр логов
docker-compose -f docker-compose.dev.yml logs -f

# Остановка проекта
docker-compose -f docker-compose.dev.yml down

# Перезапуск проекта
docker-compose -f docker-compose.dev.yml restart
```

### Prod окружение
```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Остановка проекта
docker-compose -f docker-compose.prod.yml down

# Перезапуск проекта
docker-compose -f docker-compose.prod.yml restart
```

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
├── nginx.conf              # Конфигурация Nginx
├── requirements.txt        # Зависимости Python
└── .env.template          # Шаблон переменных окружения
```

## Особенности конфигурации

### Dev окружение
- Использует Django runserver
- Включен режим отладки
- Монтирует локальные файлы для удобства разработки
- Использует отдельные тома для dev окружения

### Prod окружение
- Использует Gunicorn
- Отключен режим отладки
- Оптимизированный Dockerfile с многоэтапной сборкой
- Настроены healthcheck для всех сервисов
- Использует Nginx как прокси-сервер
- Настроено кэширование статических файлов через Whitenoise

### База данных
- Данные сохраняются в именованных томах
- Отдельные тома для dev и prod окружений
- Настроены healthcheck для проверки доступности

### Безопасность
- Используется непривилегированный пользователь в контейнере
- Переменные окружения вынесены в .env файл
- Настроены CORS заголовки

## Лицензия

MIT 