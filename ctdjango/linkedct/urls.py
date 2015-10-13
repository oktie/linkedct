#
# Copyright 2009-2015 Oktie Hassanzadeh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from django.conf.urls import url
from django.views.decorators.vary import vary_on_headers
import databrowse
from models import *
import update
import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),

    # Search.
    url(r'^search/(?P<object_type>\w+)/(?P<keyword>.+)/$', views.SearchResultView.as_view(),
        name='search'),
    url(r'^search/(?P<object_type>\w+)/$', views.search_form,
        name='search_form'),

    # Add new xml file.
    url(r'^processxml/(?P<url>.+)/$', views.process_xml,
        name='processxml'),

    # Re-process or add an xml file.
    url(r'^reprocessxml/(?P<url>.+)/$', views.reprocess_xml,
        name='reprocessxml'),

    # Display the form to select a xml file.
    url(r'^uploadxml/$', views.upload_xml,
        name='uploadxml'),

    url(r'^uploadxml/$', views.upload_xml,
        name='uploadxml'),

    # Add new xml file.
    url(r'^loadsource/(?P<source_name>.+)/$', views.load_external_source,
        name='loadsource'),

    # Databrowse
    url(r'^resource/(.*)', databrowse.site.root),

    # RDF and vocab
    url(r'^data/(.*)', views.rdf_view),

    url(r'^vocab/(.*)', views.vocab_view),

    url(r'^sparql/(.*)', views.sparql_view),

    url(r'^geosearch/$', views.map_view),

    url(r'^geosearch/results/', views.map_search_result_view),

    url(r'^fuzzy_search/$', views.fuzzy_search_view),

    url(r'^fuzzy_search/', views.fuzzy_search_view),
]
