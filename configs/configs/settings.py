"""
confi.gs project configuration
"""
# stdlib
import os
# django
from django.core.exceptions import ImproperlyConfigured

insecure_default_settings = {
    'CONFIGS_DATABASE_PASSWORD': 'configs',
    'CONFIGS_DJANGO_DEBUG': True,
    'CONFIGS_SECURITY_ALLOWED_HOSTS': '*',
    'CONFIGS_SECURITY_CSRF_COOKIE_SECURE': False,
    'CONFIGS_SECURITY_SEESION_COOKIE_SECURE': False,
    'CONFIGS_SECURITY_SECRET_KEY': 'InSecureDefaultNeverUseItInProduction!',
}
insecure_settings = []


def any2bool(obj):
    """
    returns a boolean based on a string.

    str('0'), str('false') and str('no') evaluate to False, others
    evaluate to bool(obj)
    """
    if isinstance(obj, str) and obj.lower() in ['0', 'false', 'no']:
        return False
    else:
        return bool(obj)


def configs_setting(setting, default=None):
    """
    returns a configuration setting, either read from the environment, from
    the insecure_default_settings dict or default.

    if the value from insecure_default_settings dict is used, the setting is
    added to insecure_settings lists.
    """
    final_setting = os.getenv(
        setting,
        insecure_default_settings.get(setting, default)
    )
    if setting in insecure_default_settings:
        if final_setting == insecure_default_settings[setting]:
            insecure_settings.append(setting)
    return final_setting


BASE_DIR = os.path.dirname(__file__)

USE_INSECURE_DEFAULTS = any2bool(configs_setting(
    'CONFIGS_USE_INSECURE_DEFAULTS', False
))

SECRET_KEY = configs_setting('CONFIGS_SECURITY_SECRET_KEY')

DEBUG = any2bool(configs_setting('CONFIGS_DJANGO_DEBUG'))

try:
    ALLOWED_HOSTS = configs_setting('CONFIGS_SECURITY_ALLOWED_HOSTS').split()
except AttributeError:
    ALLOWED_HOSTS = None

ENCDATA_FIELDS = configs_setting(
    'CONFIGS_ENCDATA_FIELDS', 'location role flavor'
).split()

# Application definition

CONFIGS_DEFAULT_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    # 3rd-party
    'tagging',
    'tastypie',
    # confi.gs
    'api',
    'common',
    'resources',
)

CONFIGS_DEBUG_APPS = (
    'debug_toolbar',
)

if DEBUG:
    INSTALLED_APPS = CONFIGS_DEFAULT_APPS + CONFIGS_DEBUG_APPS
else:
    INSTALLED_APPS = CONFIGS_DEFAULT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'configs.urls'

WSGI_APPLICATION = 'configs.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': configs_setting(
            'CONFIGS_DATABASE_SCHEMA', 'configs'
        ),
        'USER': configs_setting(
            'CONFIGS_DATABASE_USER', 'configs'
        ),
        'PASSWORD': configs_setting(
            'CONFIGS_DATABASE_PASSWORD',
        ),
        'HOST': configs_setting(
            'CONFIGS_DATABASE_HOST', '127.0.0.1'
        ),
        'PORT': configs_setting(
            'CONFIGS_DATABASE_PORT', '5432'
        ),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_ROOT = configs_setting('CONFIGS_DJANGO_STATIC_ROOT')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)

CSRF_COOKIE_SECURE = any2bool(configs_setting(
    'CONFIGS_SECURITY_CSRF_COOKIE_SECURE'
))

SESSION_COOKIE_SECURE = any2bool(configs_setting(
    'CONFIGS_SECURITY_SEESION_COOKIE_SECURE'
))

FORCE_LOWERCASE_TAGS = True

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'
LOGIN_REDIRECT_URL = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TASTYPIE_DEFAULT_FORMATS = ['json', 'yaml']

# if we do not explicitly accept insecure defaults, raise an error
# when insecure defaults are used
if not USE_INSECURE_DEFAULTS:
    if insecure_settings:
        raise ImproperlyConfigured(
            'Refuse to start with insecure default settings: %s' %
            ', '.join(insecure_settings)
        )
