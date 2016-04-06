"""
configs project urls
"""
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change
from django.views.generic import RedirectView
from resources import urls as resources_urls
from api import urls as api_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
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
    url(r'^api/', include(api_urls)),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('resources:network-list'),
                                    permanent=False),
        name='home'),
    url(r'^res/', include(resources_urls, namespace='resources'))
]
