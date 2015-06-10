import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

paths = ['/u/oktie/code/linkedct','/u/oktie/code/linkedct/ctdjango']
for path in paths:
   if path not in sys.path:
      sys.path.append(path)
