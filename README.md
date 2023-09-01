# backend for Agricultural Machinery Rental
[![Build Status](https://github.com/agricultural-machinery-rental/agricultural-machinery-rental-backend/actions/workflows/agriculture_backend_workflow.yaml/badge.svg)](https://github.com/agricultural-machinery-rental/agricultural-machinery-rental-backend/actions/workflows/agriculture_backend_workflow.yaml/)
[![Build Status](https://github.com/agricultural-machinery-rental/agricultural-machinery-rental-backend/actions/workflows/prod.workflow.yml/badge.svg)](https://github.com/agricultural-machinery-rental/agricultural-machinery-rental-backend/actions/workflows/prod.workflow.yml)

## Описание:
API для проекта по аренде сельскохозяйственной техники.

## Технологии:
- Python 3.10
- Django 4.2.3
- Django REST Framework 3.14.0
- Simple JWT 5.2.2

## Для разработчиков:
#### Основные данные:
- база данных по умолчанию: Postgres;
- файл зависимостей: "requirements.txt".

#### Приложения:
- _config_: общие настройки проекта;
- _api_: API;
- _core_: константы проекта.

- users
- machineries
- orders

#### Пример файла с переменными среды:
".env.example" в ./src:

#### Линтер:
Мы используем `black`.

#### PRs:
ВАЖНО! Перед перед загрузкой ветки на удаленный репозиторий сделать pre-commit для проверки оформления кода.
Для слияния с веткой develop необходимо ревью минимум двух участников проекта.

#### Схема базы данных
Будет размещена позднее

## Запуск приложения
Для запуска приложения необходим `Docker`. Для операционной системы Windows необходимо установить и активировать WSL2 (https://docs.docker.com/desktop/wsl/).

```команды для запуска проекта
docker-compose up
```
Выполняется из корневой папки проекта.
