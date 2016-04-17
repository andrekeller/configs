"""
confi,gs project urls
"""
# django
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import password_change
from django.views.generic import RedirectView
# confi.gs
from common import urls as common_urls
from resources import urls as resources_urls
from api import urls as api_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    url(r'^auth/login/$',
        login,
        {
            'template_name': 'auth/login.html',
        },
        name='login'
        ),
    url(r'^auth/logout/$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'
        ),
    url(r'^auth/password-change/$',
        password_change,
        {
            'template_name': 'auth/password_change_form.html',
            'post_change_redirect': '/',
        },
        name='password_change'
        ),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('resources:network-list'),
                                    permanent=False),
        name='home'),
    url(r'^common/', include(common_urls, namespace='common')),
    url(r'^res/', include(resources_urls, namespace='resources')),
]
