# Телеграмм бот для продажи
Этот проект представляет собой пример того, как создать Telegram бота для продажи на Python, используя библиотеку Aiogram. Кроме того, реализована панель администрирования товара на FastApi с интеграцией sqladmin.

## Особенности
- **Интеграция Aiogram**: Использование библиотеки Aiogram для создания функциональных и интерактивных Telegram ботов.
- **Панель администрирования**: FastApi вместе с sqladmin для эффективного и удобного администрирования пользователей, товара и транзакций.

## Интерфейс бота:

1. Демонстрация информативных команд:

https://github.com/SyanOSee/shopping_tg/assets/69969678/8c2e1b8a-89a9-4b7a-938f-d5b002ed9cf1


2. Демонстрация работы с корзиной и каталогами:

https://github.com/SyanOSee/shopping_tg/assets/69969678/c45cad9e-4dec-4332-8cf2-9e7daf891130

3. Оплата товара (К сожалению Telegram запрещает делать скриншоты или записывать экран после успешной оплаты):

https://github.com/SyanOSee/shopping_tg/assets/69969678/407a1f7d-6663-4a51-be32-7e211d99161c

4. Получение ссылки на админ-панель:

https://github.com/SyanOSee/shopping_tg/assets/69969678/7ca00611-6ec4-43c4-9e93-c37177f38668


## Интерфейс админ панели

https://github.com/SyanOSee/shopping_tg/assets/69969678/347584ff-a7d4-477c-93f3-cb8245f3783d


## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SyanOSee/shopping_tg
```

2. Создайте .env файлы и измините настройки в файлах Dockerfile.

3. Запустите контейнеры:
```bash
docker-compose up --build
```
