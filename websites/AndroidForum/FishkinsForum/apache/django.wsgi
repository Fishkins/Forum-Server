import os
import sys

sys.path.append('/home/fishkins/Template')
sys.path.append('/home/fishkins/websites/AndroidForum/FishkinsForum')
sys.path.append('/home/fishkins/websites/AndroidForum')

os.environ['DJANGO_SETTINGS_MODULE'] = 'FishkinsForum.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
