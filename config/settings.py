from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


DEBUG = True


ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # подключение статических файлов к проекту
    "restaurant.apps.RestaurantConfig",
    "users.apps.UsersConfig",
    "django_countries",
    "django_celery_beat",
    "corsheaders",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"


TIME_ZONE = "Europe/Moscow"


USE_I18N = True


USE_TZ = True

# префикс URL-адреса для статических файлов
STATIC_URL = "static/"


# загрузки в папку с сайта
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# список дополнительных (нестандартных) путей к статическим файлам,
# используемых для сбора и для режима отладки
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# путь к общей статической папке, формируемой при запуске команды collectstatic
# (для сбора всей статистики в единый каталог при размещении сайта на веб-сервисе)
STATIC_ROOT = os.path.join(BASE_DIR, "/static/")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "users.User"
LOGIN_URL = "users:login"

# User authentication settings
LOGIN_REDIRECT_URL = "restaurant:index"
LOGOUT_REDIRECT_URL = "restaurant:index"


# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False) == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False) == "True"


# Celery
# URL-адрес брокера сообщений
CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL"
)  # Например, Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

# Часовой пояс для работы Celery
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE")

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = os.getenv("CELERY_TASK_TRACK_STARTED")

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = os.getenv(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"
)
CELERY_BEAT_SCHEDULE = {
    "cancel-expired-bookings-every-5-minutes": {
        "task": "restaurant.tasks.cancel_expired_bookings",
        "schedule": 300,  # каждые 5 минут = 300 секунд
    },
}


# Настройки срока действия токенов
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
