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

import re

from django import http
from django import shortcuts
from django import template
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core import urlresolvers
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import databrowse
from databrowse.datastructures import *

import forms
from models import *
import models
import operations
import rdf
import hashlib
import urllib2
import urllib

import csv

from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from geopy import geocoders, distance
import math
import time
import json
import string
CONFIG = settings.CONFIG

class HttpResponseSeeOther(http.HttpResponseRedirect):
    status_code = 303

def homepage(request):
    model_list = [ Trial, Intervention, Condition,
               Country, City, State, Location,
               Eligibility, Keyword, Mesh_term,
               Condition_browse, Intervention_browse,
               Reference, Link, Investigator, Responsible_party,
               Outcome, Arm_group,
               Contact, Address, Facility, Oversight_info,
               Overall_official, Sponsor, Sponsor_group,
               Provenance ]
#    easy_model_list = [EasyModel(model) for model in model_list]
    flat_page_model = FlatPage
#    return shortcuts.render_to_response('homepage.html',
#        {'model_list': easy_model_list, 'flat_page_model': flat_page_model,
#         'upload_form': forms.XMLSelectForm()})

    #m_list = [EasyModel(databrowse.site, m) for m in databrowse.site.registry.keys()]
    databrowse.site.root_url = CONFIG['ROOT']
    m_list = [EasyModel(databrowse.site, m) for m in model_list]
    return shortcuts.render_to_response('databrowse/homepage.html', {'model_list': m_list, 'root_url': databrowse.site.root_url, 'flat_page_model': flat_page_model})

#def gen_view(request, **kwargs):
#    return list_detail.object_detail(request, **kwargs)

@vary_on_headers('Accept', 'User-Agent')
def multi_format_object_detail(request, **kwargs):
    """A view that handles multiple format output.

    By default, the view use object_detail generic view to output. If HTTP
    request parameter format is set to rdf, redirect the output to D2R server.
    """

    # For pubentry, the type is passed in but we really don't need it. If we
    # don't remove it, object_detail is going to complain about extra field
    # 'type'.
    if kwargs.get('type', None) is not None:
        kwargs.pop('type')

    if 'uid' in kwargs:
        uid_or_slug = kwargs['uid']
        kwargs.pop('uid')
    else:
        uid_or_slug = kwargs['slug']

    # Serve the RDF page if the user explicitly wants RDF.
    if request.GET.get('format', '').lower() == 'rdf':
        rdf_url = '%s%s/%s' % (CONFIG['RDF_SERVER'],
                               kwargs['extra_context']['model'].name(),
                                uid_or_slug)
        # For debugging purpose, if redirect=1 is specified, we redirect
        # to the d2r server. Otherwise, we load the RDF output from the d2r
        # server and return to the user.
        if request.GET.get('redirect'):
            #return HttpResponseSeeOther(rdf_url)
            response = http.HttpResponse(content="", status=303, status_code=303)
            response["Location"] = rdf_url
            return response
        else:
            rdf_content = rdf.load_rdf_from_url(rdf_url)
            return http.HttpResponse(rdf_content, mimetype='text/rdf+xml', status=303, status_code=303)

    # Serve the XML page if the user explicitly wants XML.
#    if request.GET.get('format', '').lower() == 'xml':
#        return cfxml(request, kwargs['extra_context']['model'].name(), uid_or_slug)

    # If it's a RDF browser, redirect to the RDF format page.
    if request.META.get('HTTP_ACCEPT', '').lower().find('rdf') != -1:
        #rdf_url = '%s%s/%s' % (CONFIG['RDF_SERVER'],
        #                       kwargs['extra_context']['model'].name(),
        #                        uid_or_slug)
        # TODO: the following is temporary solution until we find a better way
        return rdf_view(request, request.path.replace('/resource/',''))
        #rdf_content = rdf.load_rdf_from_url(rdf_url)
        #return http.HttpResponse(rdf_content,
        #return rdf_view()
        #return HttpResponseSeeOther(request.path + '?format=rdf')

    # If template_name is not set, use the default base_detail.html template.
    if not kwargs.get('template_name'):
        kwargs['template_name'] = 'base_detail.html'

    return list_detail.object_detail(request, **kwargs)
    #return gen_view(request, **kwargs)



#def cfxml(request, modelname, slug):
#    """show xml view for a given slug. (currently not working)"""
#    rtv = ""
#    t = template.loader.get_template('trial_xml.xml')
#
#    if modelname == "trial":
#        trials = Trial.objects.filter(author__slug=slug)
##    else:
##        papers = PubAuthor.objects.filter(author__slug=slug)
#        for t in trials:
#            trial = t.pubentry
#            if not trial.pid:
#                trial.pid = trial.title.replace(" ", "")
#            c = template.Context({ 'object': trial })
#            rtv += t.render(c) + "\n\n"
#    else:
#        if modelname == "provenance":
#            papers = Trial.objects.filter(provenance__slug=slug)
#        elif modelname == "xxx":
#            papers = xxx.objects.filter(series__slug=slug)
#        else:
#            return http.HttpResponse("not yet implemented for " + modelname)
#
#        for t in trials:
#            trial = t.pubentry
#            if not trial.pid:
#                trial.pid = trial.title.replace(" ", "")
#            c = template.Context({ 'object': trial })
#            rtv += t.render(c) + "\n\n"
#
#    return http.HttpResponse(rtv, mimetype="text/plain")




# Displaying a search form is simple enough that we should disable cross-site
# attack protection.
@csrf_exempt
def search_form(request, object_type):
    """Display a form so that the user can perform search actions."""
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            return http.HttpResponseRedirect(
                urlresolvers.reverse('search', args=[object_type, keyword]))
    else:
        form = forms.SearchForm()

    return shortcuts.render_to_response('search_form.html',
        {'form': form},
        context_instance=template.RequestContext(request))


class SearchResultView(ListView):

    template_name = 'databrowse/model_detail.html'

    def get_queryset(self):
        '''
        object_type: One of (pub, author, journal, series, school, keyword).
        keyword: The keyword to search for.
        '''
        object_type = self.kwargs['object_type']
        keyword = self.kwargs['keyword']
        model = getattr(models, object_type.capitalize())
        matched_objects = model.objects.filter(label__icontains=keyword)
        return matched_objects

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        self.queryset = self.get_queryset()
        model = getattr(models, self.kwargs['object_type'].capitalize())
        easy_model = EasyModel(databrowse.site, model)
        easy_qs = self.queryset._clone(klass=EasyQuerySet)
        easy_qs._easymodel = easy_model
        databrowse.site.root_url = CONFIG['ROOT']
        extra_context = {'model': easy_model,
                         'root_url': databrowse.site.root_url,
                         'request': self.request,
                         'objectlist': easy_qs}
        context.update(extra_context)
        return context


@csrf_exempt
def upload_xml(request):
    """Display a form so the user can select a xml file.

    When the form is submitted, redirects to process_xml to process the
    xml file.
    """
    if request.method == 'POST':
        form = forms.XMLSelectForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            return http.HttpResponseRedirect(
                urlresolvers.reverse('processxml', args=[url]) +
                '?encoding=' + form.cleaned_data['encoding'])
    else:
        form = forms.XMLSelectForm()

    return shortcuts.render_to_response('form_upload_xml.html',
        {'form': form},
        context_instance=template.RequestContext(request))



def load_external_source(request, source_name):
    """Loads an external source."""

    ## Loading DBpedia
    if source_name == 'dbpedia':
        for m in External_resource.objects.filter(source_name='dbpedia'):
            m.delete()
        ## Loading diseases
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'dbpedia_disease.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            try:
                id_index = row.index('id')
            except:
                return http.HttpResponse("Error finding the right column in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    resource_url = 'http://dbpedia.org/resource/' + id
                    resource_label = id.replace('_',' ')
                    resource_format = 'RDF_HTML'
                    related_model_name = 'Condition'
                    label = id + ' (dbpedia disease resource)'
                    if len(label)>127:
                        label = hashlib.md5(label).hexdigest()
                    external_resource, created = models.External_resource.objects.get_or_create(
                                    label = label,
                                    source_id = id,
                                    source_label = resource_label,
                                    source_name = source_name,
                                    source_url = resource_url,
                                    source_format = resource_format,
                                    related_model_name =related_model_name,
                                    )
                except StopIteration:
                    row = None

        ## Loading drugs
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'dbpedia_drugs.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            try:
                id_index = row.index('id')
            except:
                return http.HttpResponse("Error finding the right column in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    resource_url = 'http://dbpedia.org/resource/' + id
                    resource_label = id.replace('_',' ')
                    resource_format = 'RDF_HTML'
                    related_model_name = 'Intervention'
                    label = id + ' (dbpedia drug resource)'
                    if len(label)>127:
                        label = hashlib.md5(label).hexdigest()
                    external_resource, created = models.External_resource.objects.get_or_create(
                                    label = label,
                                    source_label = resource_label,
                                    source_id = id,
                                    source_name = source_name,
                                    source_url = resource_url,
                                    source_format = resource_format,
                                    related_model_name =related_model_name,
                                    )
                except StopIteration:
                    row = None
        return http.HttpResponse("{'status':'OK'}")

    ## Loading Drugbank
    elif source_name == 'drugbank':
        for m in External_resource.objects.filter(source_name='drugbank'):
            m.delete()
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'drugbank_drugs.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            name_index = 1
            try:
                id_index = row.index('id')
                name_index = row.index('name')
            except:
                return http.HttpResponse("Error finding the right column(s) in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    name = row[name_index]
                    resource_url = 'http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/' + id
                    resource_label = name
                    resource_format = 'RDF_HTML'
                    related_model_name = 'Intervention'
                    label = id + ' (drugbank drug resource)'
                    if len(label)>127:
                        label = hashlib.md5(label).hexdigest()
                    external_resource, created = models.External_resource.objects.get_or_create(
                                    label = label,
                                    source_label = resource_label,
                                    source_url = resource_url,
                                    source_format = resource_format,
                                    source_name = source_name,
                                    related_model_name =related_model_name,
                                    )
                except StopIteration:
                    row = None

        # alternative names
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'drugbank_drug_brandnames.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            name_index = 1
            try:
                id_index = row.index('id')
                name_index = row.index('name')
            except:
                return http.HttpResponse("Error finding the right column(s) in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    altname = unicode(row[name_index],errors='ignore')
                    alt_name, created = models.Alt_name.objects.get_or_create(
                                    label = hashlib.md5(source_name+id+altname).hexdigest(),
                                    source = source_name,
                                    id = id,
                                    altname = altname,
                                    )
                except StopIteration:
                    row = None
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'drugbank_drug_synonyms.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            name_index = 1
            try:
                id_index = row.index('id')
                name_index = row.index('name')
            except:
                return http.HttpResponse("Error finding the right column(s) in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    altname = unicode(row[name_index],errors='ignore')
                    alt_name, created = models.Alt_name.objects.get_or_create(
                                    label = hashlib.md5(source_name+id+altname).hexdigest(),
                                    source = source_name,
                                    id = id,
                                    altname = altname,
                                    )
                except StopIteration:
                    row = None

        return http.HttpResponse("{'status':'OK'}")

    ## Loading Dailymed
    elif source_name == 'dailymed':
        for m in External_resource.objects.filter(source_name='dailymed'):
            m.delete()
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'dailymed_drugs.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            name_index = 1
            try:
                id_index = row.index('id')
                name_index = row.index('name')
                fullName_index = row.index('fullName')
                activeIngridient_index = row.index('activeIngridient')
                drugbank_id_index = row.index('drugbank_id')
                genericMedicine_index = row.index('genericMedicine')
            except:
                return http.HttpResponse("Error finding the right column(s) in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    name = row[name_index]
                    resource_url = 'http://www4.wiwiss.fu-berlin.de/dailymed/resource/drugs/' + id
                    resource_label = name
                    resource_format = 'RDF_HTML'
                    related_model_name = 'Intervention'
                    label = id + ' (dailymed drug resource)'
                    if len(label)>127:
                        label = hashlib.md5(label).hexdigest()
                    external_resource, created = models.External_resource.objects.get_or_create(
                                    label = label,
                                    source_label = resource_label,
                                    source_url = resource_url,
                                    source_format = resource_format,
                                    source_name = source_name,
                                    related_model_name =related_model_name,
                                    )
                    # alternative names
                    altname = row[genericMedicine_index]
                    alt_name, created = models.Alt_name.objects.get_or_create(
                                    label = hashlib.md5(source_name+id+altname).hexdigest(),
                                    source = source_name,
                                    id = id,
                                    altname = altname,
                                    )
                    altname = row[fullName_index]
                    alt_name, created = models.Alt_name.objects.get_or_create(
                                    label = hashlib.md5(source_name+id+altname).hexdigest(),
                                    source = source_name,
                                    id = id,
                                    altname = altname,
                                    )
                    altname = row[activeIngridient_index]
                    alt_name, created = models.Alt_name.objects.get_or_create(
                                    label = hashlib.md5(source_name+id+altname).hexdigest(),
                                    source = source_name,
                                    id = id,
                                    altname = altname,
                                    )
                    altname = row[drugbank_id_index]
                    alt_name, created = models.Alt_name.objects.get_or_create(
                                    label = hashlib.md5(source_name+id+altname).hexdigest(),
                                    source = source_name,
                                    id = id,
                                    altname = altname,
                                    )
                except StopIteration:
                    row = None

        return http.HttpResponse("{'status':'OK'}")

    ## Loading diseasome
    elif source_name == 'diseasome':
        for m in External_resource.objects.filter(source_name='diseasome'):
            m.delete()
        inputfilename = CONFIG.get('SOURCES_FILE_LOC') + 'diseasome_disease.csv'
        inputfile = file(inputfilename,'r')
        csv_reader = csv.reader(inputfile, delimiter=',', quotechar='"')
        row = csv_reader.next()
        if not csv_reader:
            return http.HttpResponse("Error reading csv file")
        else:
            id_index = 0
            name_index = 1
            try:
                id_index = row.index('id')
                name_index = row.index('name')
            except:
                return http.HttpResponse("Error finding the right column(s) in the csv file")
            while row:
                try:
                    row = csv_reader.next()
                    id = row[id_index]
                    name = row[name_index]
                    resource_url = 'http://www4.wiwiss.fu-berlin.de/diseasome/resource/diseases/' + id
                    resource_label = name
                    resource_format = 'RDF_HTML'
                    related_model_name = 'Condition'
                    label = id + ' (diseasome disease resource)'
                    if len(label)>127:
                        label = hashlib.md5(label).hexdigest()
                    external_resource, created = models.External_resource.objects.get_or_create(
                                    label = label,
                                    source_label = resource_label,
                                    source_url = resource_url,
                                    source_format = resource_format,
                                    source_name = source_name,
                                    related_model_name =related_model_name,
                                    )
                except StopIteration:
                    row = None
        return http.HttpResponse("{'status':'OK'}")

    ## Other sources
    else:
        return http.HttpResponse("{'status':'FAIL', 'reason':'Source %s not found'}" % source_name)


def reprocess_xml(request, url):
    """Re-process an XML file."""
    try:
        operations.process_xml(
            url, CONFIG['XML_SIZE_LIMIT'],
            request.META['REMOTE_ADDR'], request.GET.get('encoding'),
            True)

        #return http.HttpResponseRedirect(
        #    urlresolvers.reverse('provenance_detail', args=[provenance.slug]))

        return http.HttpResponse("OK")
#        return shortcuts.render_to_response('error.html', {'content': 'OK'})


    except (operations.FileSizeLimitExceededException,
            operations.XMLFileFormatException,
            operations.FileSizeLimitExceededException), e:
        return shortcuts.render_to_response('error.html', {'content': str(e)})

def process_xml(request, url):
    """Process an XML file."""
    try:
        operations.process_xml(
            url, CONFIG['XML_SIZE_LIMIT'],
            request.META['REMOTE_ADDR'], request.GET.get('encoding'),
            False)

        #return http.HttpResponseRedirect(
        #    urlresolvers.reverse('provenance_detail', args=[provenance.slug]))

        return http.HttpResponse("OK")
#        return shortcuts.render_to_response('error.html', {'content': 'OK'})


    except (operations.FileSizeLimitExceededException,
            operations.XMLFileFormatException,
            operations.FileSizeLimitExceededException), e:
        return shortcuts.render_to_response('error.html', {'content': str(e)})

def rdf_view(request, url):
    """Provides RDF view by redirection to D2R server."""
    try:
        home_url = CONFIG["HOME"]
        d2rserver_url = CONFIG['D2R_SERVER']

        rdf_url = url
        if url.endswith('/'):
            rdf_url = url[:-1]
        rdf_url = d2rserver_url + 'data/' + rdf_url

        try:
            #request = urllib.urlopen(rdf_url)
            req = urllib2.Request(url=rdf_url)
            req.add_header("Accept","application/rdf+xml")
            request = urllib2.urlopen(req)

            response = http.HttpResponse(request.read().replace(d2rserver_url,home_url+'/').replace('/vocab/resource/','/vocab/').replace(CONFIG['D2RMAP'],''), mimetype='text/rdf+xml')
            filename = url.replace('/','-') +'.rdf'
            response['Content-Disposition'] = 'inline; filename='+ filename.replace('-.','.')
            response['Content-Type'] = 'application/rdf+xml'
            return response
        except Exception, e:
            return shortcuts.render_to_response('error.html', {'content': str(e)})

    except (operations.FileSizeLimitExceededException,
            operations.XMLFileFormatException,
            operations.FileSizeLimitExceededException), e:
        return shortcuts.render_to_response('error.html', {'content': str(e)})

def vocab_view(request, url):
    """Provides view for Vocabulary by redirection to D2R server."""
    try:
        home_url = CONFIG["HOME"]
        d2rserver_url = CONFIG['D2R_SERVER']

        rdf_url = url
        if url.endswith('/'):
            rdf_url = url[:-1]
        rdf_url = d2rserver_url + 'vocab/data/' + rdf_url

        try:
            #request = urllib.urlopen(rdf_url)
            req = urllib2.Request(url=rdf_url)
            req.add_header("Accept","application/rdf+xml")
            request = urllib2.urlopen(req)

            response = http.HttpResponse(request.read().replace(d2rserver_url,home_url+'/'), mimetype='text/rdf+xml')
            filename = url.replace('/','-') +'.rdf'
            response['Content-Disposition'] = 'inline; filename='+ filename.replace('-.','.')
            response['Content-Type'] = 'application/rdf+xml'
            return response
        except Exception, e:
            return shortcuts.render_to_response('error.html', {'content': str(e)})
    except Exception, e:
        return shortcuts.render_to_response('error.html', {'content': str(e)})

def sparql_view(request, url):
    """Provides view for sparql endpoint."""
    try:
        home_url = CONFIG["HOME"]
        d2rserver_url = CONFIG['D2R_SERVER']
        query = request.GET.get('query')
        #print query
        if query:
            rdf_url = d2rserver_url + 'sparql?query=' + query
            #print rdf_url

            try:
                request = urllib.urlopen(rdf_url)
                response = http.HttpResponse(request.read().replace(d2rserver_url,home_url+'/'), mimetype='text/rdf+n3')
                response['Content-Disposition'] = 'inline; filename=query_result.rdf'
                return response
            except Exception, e:
                return shortcuts.render_to_response('error.html', {'content': str(e)})
        else:
            return shortcuts.render_to_response('error.html', {'content': 'Query not given.'})
    except Exception, e:
        return shortcuts.render_to_response('error.html', {'content': str(e)})

def snorql_view(request, url):
    """Provides view for snorql interface."""
    try:
        home_url = CONFIG["HOME"]
        d2rserver_url = CONFIG['D2R_SERVER']
        query = request.GET.get('QUERY_STRING')
        #print '***URL:' + str(url)
        #print '***REQUEST:' + str(request)
        #print '***QUERY:' + str(query)
        if query:
            rdf_url = d2rserver_url + 'snorql/index.html?' + query + '/'
        else:
            rdf_url = d2rserver_url + 'snorql/' + url
        #print rdf_url

        try:
            request = urllib.urlopen(rdf_url)
            response = http.HttpResponse(request.read().replace(d2rserver_url,home_url+'/'))
            #response = http.HttpResponse(request.read())
            return response
        except Exception, e:
            return shortcuts.render_to_response('error.html', {'content': str(e)})
    except Exception, e:
        return shortcuts.render_to_response('error.html', {'content': str(e)})

def generate_object_list(model, queryset=None):
    """Generates an object for generic view use."""
    if queryset is None:
        queryset = model.objects.all()
    return {
        'queryset': queryset,
        'extra_context': {'model': EasyModel(model)}}


def map_view(request):

    databrowse.site.root_url = CONFIG['ROOT']
    countries = Country.objects.all().order_by('country_name')

    country = 'Canada'
    city = 'Toronto'
    dist = '5'
    condition = ''

    input_error = False
    geo_error = False
    over_max = False
    no_result = False
    error = False

    inputs = request.GET
    if ('country' in inputs) and ('city' in inputs) and ('distance' in inputs) and ('condition' in inputs):

        country = inputs.get('country')
        city = inputs.get('city')
        dist = inputs.get('distance')
        condition = inputs.get('condition')


        if not country or not city or not dist or not condition:
            input_error = True


        elif float(dist) > 50 or float(dist) < 0:
            over_max = True

        else:
            g = geocoders.GoogleV3()
            try:
                _, (lat, lng) = g.geocode(city+','+country, exactly_one=False)[0]
            except:
                geo_error = True
                error = True


            radius = float(dist)
            if not error:
                lat_diff = radius/69
                lng_diff = radius/abs(math.cos(math.radians(lat))*69)
                lat1 = str(lat - lat_diff)
                lat2 = str(lat + lat_diff)
                lng1 = str(lng - lng_diff)
                lng2 = str(lng + lng_diff)
                coords = Coordinates.objects.select_related('address', 'latitude', 'longitude', 'address__country__country_name').\
                                             filter(address__country__country_name = country,
                                                    latitude__range=(lat1, lat2),
                                                    longitude__range=(lng1,lng2)).values_list('address', 'latitude', 'longitude')

                within = []
                for c in coords:
                    if distance.distance((lat,lng), (float(c[1]),float(c[2]))).miles < radius:
                        within.append(c)

                if not within:
                    no_result = True
                    error = True

            if not error:
                conds = Condition.objects.select_related('label', 'slug').filter(label__icontains=condition).values_list('slug', flat=True)
                trials = Trial.objects.only('conditions__slug').filter(conditions__slug__in=conds).distinct()

                if not trials:
                    no_result = True
                    error = True


            trials_dict = {}
            if not error:
                for c in within:
                    ts = trials.filter(locations__facility__address__in = [c[0]])[:4].count()
                    if ts:
                        trials_dict[c] = ts
                if not trials_dict:
                    no_result = True
                    error = True


            if not error:
                return shortcuts.render_to_response('map_results.html',
                       {'coordinates': (lat, lng),  'trials': trials_dict.items(), 'countries': countries,
                        'country':country, 'city':city, 'distance':dist, 'condition':condition, 'root_url': databrowse.site.root_url})

    return shortcuts.render_to_response('map.html',
           {'input_error': input_error, 'geo_error': geo_error, 'over_max': over_max, 'no_result': no_result,
            'countries': countries, 'country':country, 'city':city, 'distance':dist,
            'condition':condition, 'root_url': databrowse.site.root_url})


def map_search_result_view(request):

    error = False
    databrowse.site.root_url = CONFIG['ROOT']

    inputs = request.GET
    if ('location' in inputs) and ('condition' in inputs):
        location_addr = inputs.get('location')
        condition = inputs.get('condition')

        if not location_addr or not condition:
            error = True

        else:
            trial_m = EasyModel(databrowse.site, Trial)
            cond_list = Condition.objects.filter(label__icontains=condition).values_list('slug', flat=True)
            trials = Trial.objects.only('locations__facility__address','conditions__slug').filter(locations__facility__address__in=[location_addr],\
            																					  conditions__slug__in=cond_list).distinct()

            facilities = []
            for t in trials:
                for l in t.locations.only('facility', 'facility__address').filter(facility__address=location_addr).distinct():
                    if l.facility.facility_name not in facilities:
                        facilities.append(l.facility.facility_name)

            facility_dict = {}
            for f in facilities:
                trial_dict = {}
                for t in trials.only('locations__facility', 'conditions').filter(locations__facility__facility_name=f):
                    trial_dict[EasyInstance(trial_m, t)] = t.conditions.all()
                facility_dict[f] = trial_dict

            return shortcuts.render_to_response('map_search_result.html',
                                                {'trials':facility_dict,
                                                 'address': Address.objects.get(slug = location_addr),
                                                 'condition': condition,
                                                 'root_url': databrowse.site.root_url})

    return shortcuts.render_to_response('map_search_result.html',
                                        {'error':error, 'root_url': databrowse.site.root_url})
