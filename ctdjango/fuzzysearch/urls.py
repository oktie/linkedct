from django.conf.urls import url
from django.conf import settings
from httpproxy.views import HttpProxy
from . import views

urlpatterns = [
    # ex: /fuzzysearch/
    url(r'^$', views.index, name='index'),
    # The proxy for SRCH2 endpoint
    url(r'^srch2/(?P<url>.*)$',
        HttpProxy.as_view(base_url=settings.CONFIG['SRCH2'])),
]
