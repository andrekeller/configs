"""
configs project configuration
"""
import configparser
import os


def str2bool(string):
    if isinstance(string, str) and string.lower() in ['0', 'false', 'no']:
        return False
    else:
        return bool(string)

BASE_DIR = os.path.dirname(__file__)

CONFIGS_INI = configparser.ConfigParser()
CONFIGS_INI.read('/etc/configs/configs.ini')

SECRET_KEY = os.getenv('CONFIGS_SECURITY_SECRET_KEY',
                       CONFIGS_INI.get('security',
                                       'secret_key',
                                       fallback='InSecureDefaultNeverUseItInProduction'
                                       )
                       )

DEBUG = str2bool(os.getenv('CONFIGS_DJANGO_DEBUG',
                           CONFIGS_INI.getboolean('django',
                                                  'debug',
                                                  fallback=True
                                                  )
                           )
                 )


ALLOWED_HOSTS = os.getenv('CONFIGS_SECURITY_ALLOWED_HOSTS',
                          CONFIGS_INI.get('security',
                                          'allowed_hosts',
                                          fallback="*"
                                          )
                          ).split()

ENCDATA_FIELDS = os.getenv('CONFIGS_CONFIGS_ENCDATA_FIELDS',
                           CONFIGS_INI.get('configs',
                                           'encdata_fields',
                                           fallback="location role flavor"
                                           )
                           ).split()

# Application definition

CONFIGS_DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'tagging',
    'tastypie',
    'api',
    'entities',
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
        'NAME': os.getenv('CONFIGS_DATABASE_SCHEMA',
                          CONFIGS_INI.get('database',
                                          'schema',
                                          fallback='configs'
                                          )
                          ),
        'USER': os.getenv('CONFIGS_DATABASE_USER',
                          CONFIGS_INI.get('database',
                                          'user',
                                          fallback='configs'
                                          )
                          ),
        'PASSWORD': os.getenv('CONFIGS_DATABASE_PASSWORD',
                              CONFIGS_INI.get('database',
                                              'password',
                                              fallback='configs'
                                              )
                              ),
        'HOST': os.getenv('CONFIGS_DATABASE_HOST',
                          CONFIGS_INI.get('database',
                                          'host',
                                          fallback='127.0.0.1'
                                          )
                          ),
        'PORT': os.getenv('CONFIGS_DATABASE_PORT',
                          CONFIGS_INI.get('database',
                                          'port',
                                          fallback='5432'
                                          )
                          ),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)
STATIC_ROOT = os.getenv('CONFIGS_DJANGO_STATIC_ROOT',
                        CONFIGS_INI.get('django',
                                        'static_root',
                                        fallback=None
                                        )
                        )
STATIC_URL = '/static/'

CSRF_COOKIE_SECURE = str2bool(
    os.getenv(
        'CONFIGS_SECURITY_CSRF_COOKIE_SECURE',
        CONFIGS_INI.getboolean(
            'security',
            'csrf_cookie_secure',
            fallback=False
        )
    )
)

SESSION_COOKIE_SECURE = str2bool(
    os.getenv(
        'CONFIGS_SECURITY_SEESION_COOKIE_SECURE',
        CONFIGS_INI.getboolean(
            'security',
            'session_cookie_secure',
            fallback=False
        )
    )
)

FORCE_LOWERCASE_TAGS = True

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'
LOGIN_REDIRECT_URL = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TASTYPIE_DEFAULT_FORMATS = ['json', 'xml', 'yaml']
