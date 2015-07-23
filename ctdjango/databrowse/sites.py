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
from django.db import models
from django.apps import apps
from databrowse.datastructures import EasyModel
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.conf import settings

from django.views.decorators.vary import vary_on_headers

CONFIG = settings.CONFIG

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class DatabrowsePlugin(object):
    def urls(self, plugin_name, easy_instance_field):
        """
        Given an EasyInstanceField object, returns a list of URLs for this
        plugin's views of this object. These URLs should be absolute.

        Returns None if the EasyInstanceField object doesn't get a
        list of plugin-specific URLs.
        """
        return None

    def model_index_html(self, request, model, site):
        """
        Returns a snippet of HTML to include on the model index page.
        """
        return ''

    def model_view(self, request, model_databrowse, url):
        """
        Handles main URL routing for a plugin's model-specific pages.
        """
        raise NotImplementedError

class ModelDatabrowse(object):
    plugins = {}

    def __init__(self, model, site):
        self.model = model
        self.site = site

    @vary_on_headers('Accept')
    def root(self, request, url):
        """
        Handles main URL routing for the databrowse app.

        `url` is the remainder of the URL -- e.g. 'objects/3'.
        """
        # Delegate to the appropriate method, based on the URL.
        if url is None:
            return self.main_view(request)
        try:
            plugin_name, rest_of_url = url.split('/', 1)
        except ValueError: # need more than 1 value to unpack
            plugin_name, rest_of_url = url, None
        try:
            plugin = self.plugins[plugin_name]
        except KeyError:
            plugin = self.plugins['objects']
            rest_of_url = url
            #raise http.Http404('A plugin with the requested name does not exist.')
        return plugin.model_view(request, self, rest_of_url)

    def main_view(self, request):
        easy_model = EasyModel(self.site, self.model)
        html_snippets = mark_safe(u'\n'.join([p.model_index_html(request, self.model, self.site) for p in self.plugins.values()]))
        return render_to_response('databrowse/model_detail.html', {
            'model': easy_model,
            'objectlist': easy_model.objects(),
            'root_url': self.site.root_url,
            'plugin_html': html_snippets,
            'request': request,
        })

class DatabrowseSite(object):
    def __init__(self):
        self.registry = {} # model_class -> databrowse_class
        self.root_url = None

    def register(self, model_or_iterable, databrowse_class=None, **options):
        """
        Registers the given model(s) with the given databrowse site.

        The model(s) should be Model classes, not instances.

        If a databrowse class isn't given, it will use DefaultModelDatabrowse
        (the default databrowse options).

        If a model is already registered, this will raise AlreadyRegistered.
        """
        databrowse_class = databrowse_class or DefaultModelDatabrowse
        if issubclass(model_or_iterable, models.Model):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self.registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            self.registry[model] = databrowse_class

    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        if issubclass(model_or_iterable, models.Model):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self.registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self.registry[model]

    def root(self, request, url):
        """
        Handles main URL routing for the databrowse app.

        `url` is the remainder of the URL -- e.g. 'comments/comment/'.
        """
        #self.root_url = request.path[:len(request.path) - len(url)]
        self.root_url = CONFIG['ROOT']
        app_label = 'linkedct'
        
        url = url.rstrip('/') # Trim trailing slash, if it exists.

        if url == '':
            return self.index(request)
        else:
            return self.model_page(request, app_label,*url.split('/', 1))

        print url
        raise http.Http404('The requested databrowse page does not exist.')

    def index(self, request):
        #m_list = [EasyModel(self, m) for m in self.registry.keys()]
        #return render_to_response('databrowse/homepage.html', {'model_list': m_list, 'root_url': self.root_url})
        from django.shortcuts import redirect
        return redirect(CONFIG['HOME'], permanent=True)

    def model_page(self, request, app_label, model_name, rest_of_url=None):
        """
        Handles the model-specific functionality of the databrowse site, delegating
        to the appropriate ModelDatabrowse class.
        """
        model = apps.get_model(app_label, model_name)
        if model is None:
            raise http.Http404("App %r, model %r, not found." % (app_label, model_name))
        try:
            databrowse_class = self.registry[model]
        except KeyError:
            raise http.Http404("This model exists but has not been registered with databrowse.")
        return databrowse_class(model, self).root(request, rest_of_url)

site = DatabrowseSite()

from databrowse.plugins.calendars import CalendarPlugin
from databrowse.plugins.objects import ObjectDetailPlugin
from databrowse.plugins.fieldchoices import FieldChoicePlugin

class DefaultModelDatabrowse(ModelDatabrowse):
    plugins = {'objects': ObjectDetailPlugin(), 'calendars': CalendarPlugin(), 'fields': FieldChoicePlugin()}
