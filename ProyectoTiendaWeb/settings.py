"""
Django settings for ProyectoTiendaWeb project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as mensajes_de_error

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i8z00p_&6#epxuyp1lts#sxdquw41qlvz@3r1es^0g7l2klm9#'

# SECURITY WARNING: don't run with debug turned on in production!
# Esto indica que estamos en modo desarollo. Cambiar una vez se quiera subir al servidor a 'False'
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ProyectoTiendaWebApp',
    'ServiciosApp',
    'ContactoApp',
    'TiendaApp',
    'CarroApp',
    'AutenticacionApp',
    'ProveedoresApp',
    'crispy_forms',
    "crispy_bootstrap5",
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

ROOT_URLCONF = 'ProyectoTiendaWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'CarroApp.context_processor.importe_total_carro', # App.archivo.nombre_de_la_funcion
            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectoTiendaWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/' # URL pública para archivos estáticos como CSS, JavaScript e imágenes que no cambian.

MEDIA_URL = '/media/' # Ruta pública que los usuarios ven en sus navegadores.

MEDIA_ROOT = (BASE_DIR / 'media') # Dónde se guardan los archivos en tu servidor.

STATICFILES_DIRS = [
    BASE_DIR / "ProyectoTiendaWebApp/static",
    BASE_DIR / "ServiciosApp/static",
    BASE_DIR / "TiendaApp/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración del Email para ElasticMail
EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.elasticemail.com'
EMAIL_PORT= 2525 # 2525 587
EMAIL_USE_TLS= True
EMAIL_HOST_USER= "tecnomarkettc@gmail.com"
EMAIL_HOST_PASSWORD= "185AF083D413D5F83C7E4F3249A9B7C8B2A1"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Depuración del envío de correo
EMAIL_USE_LOCALTIME = True
EMAIL_DEBUG = True

# CrispyForms
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Mensajes de errores
MESSAGE_TAGS= {

    mensajes_de_error.DEBUG: 'debug',
    mensajes_de_error.INFO: 'info',
    mensajes_de_error.SUCCESS: 'success',
    mensajes_de_error.WARNING: 'warning',
    mensajes_de_error.ERROR: 'danger',

}

