# Сайт для бронирования столиков в ресторане 
### Описание задачи:
Необходимо создать сайт для бронирования столиков в ресторане. Сайт должен быть сверстан и подключен к админке. Для выполнения задачи необходимо использовать Django и Bootstrap. Сайт должен содержать основные разделы, необходимые для бронирования столиков и управления бронированиями.
### Задача:
1. Сверстать сайт для бронирования столиков.
2. Подключить сайт к админке Django.
3. Использовать Bootstrap для создания адаптивного и привлекательного интерфейса.
### Функционал сайта:
1. **Главная страница**:
    - [x] Описание ресторана.
    - [x] Перечень предоставляемых услуг.
    - [x] Контактная информация.
    - [x] Форма для обратной связи.
2. **Страница "О ресторане"**:
    - [x] История ресторана.
    - [x] Миссия и ценности.
    - [x] Команда.
3. **Страница бронирования**:
    - [x] Форма для бронирования столика.
    - [x] Просмотр доступности столиков.
    - [x] Подтверждение бронирования.
4. **Личный кабинет**:
    - [x] Регистрация и авторизация пользователей.
    - [x] Просмотр истории бронирований.
    - [x] Управление текущими бронированиями (изменение, отмена).
5. **Админка**:
    - [x] Управление пользователями.
    - [x] Управление бронированиями.
    - [x] Управление контентом сайта (тексты, изображения и т.д.).
### **Технические требования**
1. **Фреймворк**:
    - [x] Использовать фреймворк Django для реализации проекта.
2. **База данных**:
    - [x] Использовать PostgreSQL для хранения данных.
3. **Фронтенд**:
    - [x] Использовать Bootstrap для создания адаптивного интерфейса.
4. **Контейнеризация**:
    - [x] Использовать Docker и Docker Compose для контейнеризации приложения.
5. **Документация**:
    - [x] В корне проекта должен быть файл README.md с описанием структуры проекта и инструкциями по установке и запуску.
6. **Качество кода**:
    - [x] Соблюдать стандарты PEP8.
    - [x] Весь код должен храниться в удаленном Git репозитории.

### **Установка и запуск**

**Предварительные условия:**

* Python 3.12
* PostgreSQL
* Redis
* Celery

### Установка:

1. **Клонирование репозитория:**

```powershell
   git clone <репозиторий_GitHub>
   cd <название_репозитория>
```

2. **Установка зависимостей:**

```bash 
   pip install -r requirements.txt
```

3. **Настройка переменных окружения:**

Создайте файл .env в корне проекта и заполните его переменными по шаблону **.env_example:**

```
DATABASE_URL=<URL_для_подключения_к_PostgreSQL>
SECRET_KEY=<секретный_ключ>
...
```

4. **Создание базы данных:**

```bash 
  python manage.py migrate
```

5. **Создание администратора:**

```bash 
  python manage.py csu
```

6. **Запуск сервера разработки:**

```bash 
   python manage.py runserver
```

7. **Запуск Celery (для отложенных задач Windows):**

```bash
   celery -A config worker -l info -P gevent
```

8. **Запуск Flower (для мониторинга Celery задач):**

```bash
   celery -A config flower --port=5555
```

### Развертывание с помощью Docker и Docker Compose

Этот проект можно легко развернуть с помощью Docker и Docker Compose. Для этого необходимо установить Docker и Docker
Compose на вашей системе.

1. **Запустите контейнеры Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Этот процесс создаст и запустит все необходимые контейнеры. Для запуска в фоновом режиме используйте:

   ```bash
   docker-compose up --build -d
   ```

2. **Примените миграции Django:**

 ```bash
   docker-compose exec app python manage.py migrate
   ```

3. **Приложение будет доступно по адресу `http://localhost:8000`.**

## Остановка и очистка

- **Остановить контейнеры:**

  ```bash
  docker-compose down
  ```

- **Очистить тома данных (если используются):**

  ```bash
  docker-compose down -v
  ```




