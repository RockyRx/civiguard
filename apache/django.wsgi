import os
import sys

sys.path.insert(0, '/var/www/html/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'testproject.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()