from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.conf import settings
CONFIG = settings.CONFIG
from linkedct.models import *
import databrowse
from databrowse.datastructures import EasyModel

@never_cache
def index(request):
    '''
    Display live stats for entity and link counts.
    '''
    model_list = [ Trial, External_linkage,
                   Country, City, State, Location, Intervention, Condition,
                   Eligibility, Keyword, Mesh_term,
                   Condition_browse, Intervention_browse,
                   Reference, Link, Investigator, Responsible_party,
                   Outcome, Arm_group,
                   Contact, Address, Facility, Oversight_info,
                   Overall_official, Sponsor, Sponsor_group,
                   Provenance ]
    databrowse.site.root_url = CONFIG['ROOT']
    m_list = [EasyModel(databrowse.site, m) for m in model_list]
    return render_to_response('stats/index.html',
        {'model_list': m_list,
        'root_url': databrowse.site.root_url,
        'flat_page_model': FlatPage})
