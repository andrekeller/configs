"""
confi.gs common urls
"""
# django
from django.conf.urls import url
# confi.gs
from .views import EntityCreate
from .views import EntityDelete
from .views import EntityList
from .views import EntityUpdate

urlpatterns = [
    url(r'^$', EntityList.as_view(), name='entity-list'),
    url(r'^new$', EntityCreate.as_view(), name='entity-new'),
    url(r'^edit/(?P<pk>\d+)$', EntityUpdate.as_view(), name='entity-edit'),
    url(r'^delete/(?P<pk>\d+)$', EntityDelete.as_view(), name='entity-delete'),
]
