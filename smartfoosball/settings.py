"""
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import dotenv
dotenv.read_dotenv()

import dj_database_url
from getenv import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i2@f=lp965p02xfb551q)v1(0=c5w5($vlm(y_(_hmhb880k(0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smartfoosball'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'smartfoosball.urls'

WSGI_APPLICATION = 'smartfoosball.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(
        env("DATABASE_URI", "mysql://root:root@localhost:3306/foosball")),
}
# store emoji
DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

LANGUAGES = (
    ('zh-CN', 'zh-CN'),
    ('en-US', 'en-US'),
)


TIME_ZONE = 'Asia/Chongqing'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = env('STATIC_URL', '/static/')

MEDIA_URL = env('MEDIA_URL', '/media/')

TOKEN = env('TOKEN', '')
WX_APPID = env('WX_APPID', '')
WX_SECRET = env('WX_SECRET', '')

PRODUCT_KEY = env('PRODUCT_KEY', '')
GW_APPID = env('GW_APPID', '')
GW_USER = env('GW_USER', '')
GW_PWD = env('GW_PWD', '')