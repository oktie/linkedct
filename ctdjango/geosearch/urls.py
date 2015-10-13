from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.map_view),
    url(r'^results/', views.map_search_result_view),
]
