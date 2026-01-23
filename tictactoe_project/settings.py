import os
from pathlib import Path
from dotenv import load_dotenv  # Importante para cargar el archivo .env

# Carga las variables del archivo .env al entorno de Python
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURACIÓN DE ANALYTICS (Puntos 5, 23, 24 y 27) ---
# Se accede a las variables usando os.environ para mantener la seguridad
GOOGLE_ANALYTICS_MEASUREMENT_ID = os.environ.get('G-DMCBPQDS9Z')
GOOGLE_ANALYTICS_STREAM_ID = os.environ.get('13312057147')
GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get('520213170')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-khov&ubuhz6uuyk4f641=i)48ubf+q)&1*a+7)cb)ll6)u^3s4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'daphne',
    'chatbot',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'games',
    'widget_tweaks',
    'rest_framework',
    'api',
    'Agify',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tictactoe_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'tictactoe_project.wsgi.application'
ASGI_APPLICATION = 'tictactoe_project.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
