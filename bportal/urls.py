# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from core.utils import download_file

from core import views as core_views

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),  # NOQA
    url(r'^accounts/', include('django.contrib.auth.urls')), # accounts
    url(r'^signup/$', core_views.signup, name='signup'), #signup custom
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'), # account activation send route
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'), # activate account route
    url(r'^employer/', include('employer.urls')),
    url(r'^employee/', include('healthquestionaire.employee_urls')),
    url(r'^crud/', include('crudbuilder.urls')),
    url(r'^sss-file/', download_file),
    url(r'^login_success/', core_views.login_success, name='login_success'),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
