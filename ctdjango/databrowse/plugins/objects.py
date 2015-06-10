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

from django import http
from databrowse.datastructures import EasyModel, EasyInstanceField
from databrowse.sites import DatabrowsePlugin
from django.shortcuts import render_to_response
import urlparse

class HttpResponseSeeOther(http.HttpResponseRedirect):
    status_code = 303

class ObjectDetailPlugin(DatabrowsePlugin):
    def model_view(self, request, model_databrowse, url):
        # If the object ID wasn't provided, redirect to the model page, which is one level up.
        
        if url is None:
            return http.HttpResponseRedirect(urlparse.urljoin(request.path, '../'))
        
        self.model = model_databrowse.model
        self.site = model_databrowse.site
        easy_model = EasyModel(self.site, self.model)
        
        url_bits = url.split('/', 1)
        if len(url_bits)>1:
            objurl = url_bits[0]
            if url_bits[1].startswith('fields/'):
                fieldname = url_bits[1][7:]
                field = self.model._meta.get_field(fieldname)
                obj = easy_model.object_by_pk(objurl)
                #if field in self.model._meta.fields:
                e = EasyInstanceField(easy_model, obj, field)
                #elif field in self.model._meta.many_to_many:
                #    e = EasyInstanceField(easy_model, obj, self.model._meta.many_to_many.get(fieldname))
                furls = e.urls()
                obj = easy_model.object_by_pk(objurl)
                print furls
                #print kos
                return render_to_response('databrowse/foreignkeychoice_list.html', {'object': obj, 'root_url': model_databrowse.site.root_url, 'model': easy_model, 'field_name': fieldname,'field_urls': furls, 'request': request})

        #elif url.find('/')!=-1:
        #    url = url[:url.find('/')]
        
        obj = easy_model.object_by_pk(url)
        
        # If it's a RDF browser, redirect to the RDF format page.
        if request.META.get('HTTP_ACCEPT', '').lower().find('rdf') != -1:
            return HttpResponseSeeOther(obj.rdf_url())
        
        return render_to_response('databrowse/object_detail.html', {'object': obj, 'root_url': model_databrowse.site.root_url, 'object_slug': url})
