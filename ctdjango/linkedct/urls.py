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

from django.conf.urls.defaults import patterns, url
import databrowse
from models import *
import update
import views


from django.views.decorators.vary import vary_on_headers
from django.conf import settings
#pubentry_list = views.generate_object_list(models.PubEntry,
#    models.PubEntry.objects.select_related(*models.SELECT_RELATED_LIST))
#author_list = views.generate_object_list(models.Author)

urlpatterns = patterns('',
    url(r'^$', views.homepage, name='homepage'),
)

# Add list and detail view for Journal, Keyword, Language, etc. Author and
# PubEntry has their special attributes and views for them are added
# separately.

model_list = [ Trial, Intervention, Condition,
               Country, City, State, Location,
               Eligibility, Keyword, Mesh_term, 
               Condition_browse, Intervention_browse,
               Reference, Link, Investigator, Responsible_party,
               Outcome, Arm_group,  
               Contact, Address, Facility, Oversight_info,  
               Overall_official, Sponsor, Sponsor_group,
               Provenance ]

#for model in model_list:
#    queryset_list = views.generate_object_list(model)
#    model_name = model._meta.verbose_name
#
#    urlpatterns += patterns('',
#        url(r'^list/' + model_name + '/$',
#            view='django.views.generic.list_detail.object_list',
#            kwargs=dict(queryset_list, template_name='base_list.html'),
#            name=model_name + '_list'),
#
#        url(r'^' + model_name + '/(?P<slug>.+)/$',
#            view=views.multi_format_object_detail,
#            kwargs=dict(queryset_list),
#            name=model_name + '_detail'),
#
##        url(r'^xml/abc/(?P<slug>.+)/$',
##            view=views.cfxml,
##            kwargs=dict(queryset_list),
##            name='author_xml'),
##        (r'^xml/abc/(?P<slug>.+)/$', 'ctdjango.linkedct.views.cfxml'),
##         (r'^xml/' + model_name + '/(?P<slug>.+)/$', views.cfxml),
#    )


#pub_types = [type[0] for type in models.PubEntry.TYPE_CHOICES]
#pub_types_regex = '|'.join(pub_types)

urlpatterns += patterns('',

    # Search.
    url(r'^search/(?P<object_type>\w+)/(?P<keyword>.+)/$', views.search,
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
    (r'^resource/(.*)', databrowse.site.root),
    
    # RDF and vocab
    (r'^data/(.*)', views.rdf_view),
    
    (r'^vocab/(.*)', views.vocab_view),
    
    (r'^sparql/(.*)', views.sparql_view),
    
    #(r'^snorql/(.*)', views.snorql_view),
    
    (r'^stats/', views.stats_view),
    
    (r'^geosearch/$', views.map_view),
    
    (r'^geosearch/results/', views.map_search_result_view),
    
    (r'^keyword_search/$', views.keyword_search_view),
    
    (r'^keyword_search/', views.keyword_search_view),    

)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve',\
        {'document_root': settings.MEDIA_ROOT}),
)

