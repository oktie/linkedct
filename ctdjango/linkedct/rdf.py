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

import urllib2
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import models


def load_rdf_from_url(url):
    try:
        request = urllib2.urlopen(url)
        content = request.read()
        return process_rdf_from_d2r(content)
    except urllib2.URLError:
        return 'Error reading from RDF Store.'


def process_rdf_from_d2r(content):
    content = content.replace(':2020/resource/', '/')
    content = content.replace(':2020/data/', '/')
    content = content.replace('/publication/', '/pub/')
    return content


def discover_author_links(author):
    """Add external links for authors."""
    dblp_authors = models.DblpAuthor.objects.filter(slug=author.slug)
#   if url_exists(url):
    if len(dblp_authors)>0:
        # DBLP Link
        models.AuthorLink.objects.get_or_create(
            author=author, url=dblp_authors[0].url, type='HTML')
        # Linked DBLP Link
        name = author.name.replace(' ', '_').replace('-', '_').replace("\\'",'').replace("'",'')
        url = 'http://dblp.l3s.de/d2r/resource/authors/%s' % name
        models.AuthorLink.objects.get_or_create(
            author=author, url=url, type='RDF')
       
    dogfood_authors = models.DogFoodAuthor.objects.filter(slug=author.slug)
#   if url_exists(url):
    if len(dogfood_authors)>0:
        models.AuthorLink.objects.get_or_create(author=author, url=dogfood_authors[0].url, type='RDF/HTML')
        
    lod_authors = models.LodAuthor.objects.filter(slug=author.slug)
    for lod_author in lod_authors:
        models.AuthorLink.objects.get_or_create(author=author, url=lod_author.url, type='RDF')


def discover_pubentry_links(pubentry):
    """Add external links for pubentries.

    Args:
      pubentry: A models.PubEntry object.
    """
    # Link to DBLP based on pid.
    if pubentry.pid[:5] == 'DBLP:':
        url = 'http://dblp.l3s.de/d2r/page/publications/' + pubentry.pid[5:]
        models.PubEntryLink.objects.get_or_create(
            pubentry=pubentry, url=url, type='rdf')


def discover_keyword_links(keyword_obj):
    """ Add links to wikipedia and dbpedia based for keywords.

    Args:
      keyword_obj: A models.Keyword object.
    """
    keyword_slug = keyword_obj.slug.replace('_', ' ').replace('-', ' ')
    buzzwords = models.BuzzWord.objects.filter(buzzword=keyword_slug)
    if len(buzzwords) > 0:
        # rxin: I am not sure if we need the for loop here since the filter
        # should return only one result, but it certainly does no harm with
        # a for loop.
        for buzzword in buzzwords.all():
            models.KeywordLink.objects.get_or_create(
                buzzword=buzzword, keyword=keyword_obj)


def url_exists(url):
    """Checks whether a URL exists."""
    return True
    validator = URLValidator(True)
    try:
        validator(url)
        return True
    except ValidationError:
        return False
