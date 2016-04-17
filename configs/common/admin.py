"""
confi.gs common admin
"""
# django
from django.contrib import admin
# confi.gs
from .models import Entity, Tag

admin.site.register(Entity)
admin.site.register(Tag)
