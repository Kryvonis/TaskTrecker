"""
Local settings. File must be named `local.py`.
In this file you must specify you credentials to db
and other variables like as DEBUG=True
"""

from .common import *

DATABASES['default'].update({
    'USER': 'user',
    'PASSWORD': 'password',
})

EMAIL_HOST_USER = 'email@mail.com'
EMAIL_HOST_PASSWORD = 'password'