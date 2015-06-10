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

from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django import http
from django import shortcuts
from django import template
from django.core import urlresolvers
from django.views.generic import list_detail
from databrowse.datastructures import EasyModel, models
import models
import forms

###########
# CHOICES #
###########

def choice_list(request, app_label, module_name, field_name, models):
    m, f = lookup_field(app_label, module_name, field_name, models)
    return render_to_response('databrowse/choice_list.html', {'model': m, 'field': f})

def choice_detail(request, app_label, module_name, field_name, field_val, models):
    m, f = lookup_field(app_label, module_name, field_name, models)
    try:
        label = dict(f.field.choices)[field_val]
    except KeyError:
        raise Http404('Invalid choice value given')
    obj_list = m.objects(**{f.field.name: field_val})
    return render_to_response('databrowse/choice_detail.html', {'model': m, 'field': f, 'value': label, 'object_list': obj_list})

