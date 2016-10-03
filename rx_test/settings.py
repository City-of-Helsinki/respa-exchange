import os

from django.utils.translation import ugettext_lazy as _
from django_jinja.builtins import DEFAULT_EXTENSIONS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "test"
INSTALLED_APPS = [
    'modeltranslation',
    'grappelli',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_jwt',
    'corsheaders',
    'easy_thumbnails',
    'image_cropping',
    'autoslug',
    'django_hstore',
    'guardian',
    'django_jinja',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'helusers.providers.helsinki',

    'munigeo',
    'helusers',

    'resources',
    'users',
    'respa_exchange',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'rx_test.urls'
WSGI_APPLICATION = 'rx_test.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'respa',  # NB: Shares a database with respa!
    }
}

LANGUAGE_CODE = 'fi'
LANGUAGES = (
    ('fi', _('Finnish')),
    ('en', _('English')),
    ('sv', _('Swedish'))
)

TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MODELTRANSLATION_FALLBACK_LANGUAGES = ('fi', 'en', 'sv')
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'fi'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media/'
DEFAULT_SRID = 4326
CORS_ORIGIN_ALLOW_ALL = True
SITE_ID = 1
RESPA_MAILS_ENABLED = False
RESPA_MAILS_FROM_ADDRESS = ""
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
)
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'extensions': DEFAULT_EXTENSIONS + ["jinja2.ext.i18n"],
            'translation_engine': 'django.utils.translation',
            "match_extension": ".jinja",
        },
    },
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
            ],
        },
    },
]
