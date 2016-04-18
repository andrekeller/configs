"""
confi.gs networkgroup urls
"""
# django
from django.conf.urls import url
# confi.gs
from resources.views import NetworkGroupCreate
from resources.views import NetworkGroupDelete
from resources.views import NetworkGroupUpdate

urlpatterns = [
    url(r'^new$', NetworkGroupCreate.as_view(), name='networkgroup-new'),
    url(r'^edit/(?P<pk>\d+)$', NetworkGroupUpdate.as_view(), name='networkgroup-edit'),
    url(r'^delete/(?P<pk>\d+)$', NetworkGroupDelete.as_view(), name='networkgroup-delete'),
]
