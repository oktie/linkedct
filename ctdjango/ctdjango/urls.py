"""ctdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.BASE_DIR, 'static'),
         'show_indexes': True}),
    # Fuzzy search app
    url(r'^fuzzysearch/', include('fuzzysearch.urls', namespace='fuzzysearch')),
    # Stats app
    url(r'^stats/', include('stats.urls', namespace='stats')),
    # Geo search app
    url(r'^geosearch/', include('geosearch.urls', namespace='geosearch')),
    # LinkedCT main app
    url(r'^', include('linkedct.urls')),
]
