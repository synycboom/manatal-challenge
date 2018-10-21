from challenge.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'file:testdb?mode=memory&cache=shared',
    }
}
