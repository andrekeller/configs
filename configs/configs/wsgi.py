"""
confi.gs project WSGI configuration
"""
# stdlib
import os
# django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")
application = get_wsgi_application()
