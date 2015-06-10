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

from django import template
from django.core import urlresolvers
from django.db import connection


register = template.Library()

@register.simple_tag
def rdf_url(value):
    "Converts an HTML URI to an RDF URI"
    return value.replace('/resource/','/data/')

register.filter('rdf_url', rdf_url)

@register.simple_tag
def url_detail_rdf(name, object):
    try:
        return (urlresolvers.reverse(name + '_detail',
                                    args=(object.type, object.slug,)) + 
                '?format=rdf')
    except AttributeError:
        return (urlresolvers.reverse(name + '_detail', args=(object.slug,)) + 
                '?format=rdf')

@register.simple_tag
def url_detail_xml(name, object):
    try:
        return (urlresolvers.reverse(name + '_detail',
                                    args=(object.type, object.slug,)) + 
                '?format=xml')
    except AttributeError:
        return (urlresolvers.reverse(name + '_detail', args=(object.slug,)) + 
                '?format=xml')

#@register.simple_tag
#def url_detail_clinicaltrials(name, object):
#    url = ""
#    try:
#        url = (urlresolvers.reverse(name + '_detail',
#                                    args=(object.type, object.slug,)) + 
#                '?format=xml')
#    except AttributeError:
#        url = (urlresolvers.reverse(name + '_detail', args=(object.slug,)) + 
#                '?format=xml')
#    return 'http://clinicaltrials.gov/show/' + name + '?displayxml=true'


@register.simple_tag
def url_detail(name, object):
    if object is None or object.slug is None or not object.slug:
        return '#'
    try:
        return urlresolvers.reverse(name + '_detail',
                                    args=(object.type, object.slug,))
    except AttributeError:
        return urlresolvers.reverse(name + '_detail', args=(object.slug,))


@register.simple_tag
def url_detail_by_uid(name, object):
    return urlresolvers.reverse(name + '_detail', args=(object.uid,))


@register.simple_tag
def url_pubentry_list_by_type(type):
    return urlresolvers.reverse('publication_list_by_type', args=(type,))


@register.simple_tag
def url_list(name):
    return urlresolvers.reverse(name + '_list')


@register.simple_tag
def cycle_no_for_loop(value1, value2):
    cycle_no_for_loop.counter += 1
    if cycle_no_for_loop.counter % 2:
        return value1
    else:
        return value2
cycle_no_for_loop.counter = 0


@register.simple_tag
def query_history():
    """Generate a list of SQL queries.
    
    This is used only for debugging. A template can include it by
    {% load linkedct %}
    {% query_history %}
    """
    result = ''
    # PyDev likes to complain about undefined connection.queries. Suppress it.
    for query in connection.queries:  #@UndefinedVariable
        result += '%s\n%s\n\n' % (query['sql'], query['time'])
    return result
