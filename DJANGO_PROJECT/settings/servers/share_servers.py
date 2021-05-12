from ..base import *

DEBUG = os.environ.get('DEBUG', False) == 'True'
# Application definition
INSTALLED_APPS += [
    # third party apps

    # my apps
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Update database configuration with $DATABASE_URL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '',
        "OPTIONS": {
            "client_encoding": 'UTF8',
        },
    },
}


CDN_URL = os.environ.get('CDN_URL', None)

MEDIA_ROOT = os.path.join(FILE_ACCESS_PATH, "media")
MEDIA_URL = "%s/%s/" % (CDN_URL, 'media')

STATIC_ROOT = os.path.join(FILE_ACCESS_PATH, 'staticfiles')
STATIC_URL = "%s/%s/" % (CDN_URL, 'staticfiles')
