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

"""
 This file contains functions that can be used to update between versions
 of linkedct.
"""

from django import http

import models
import rdf


#def discover_condition_links(request):
#    for pubentry in models.Condition.objects.all():
#        rdf.discover_condition_links(pubentry)
#    return http.HttpResponse("Done!")
#
#
#def discover_intervention_links(request):
#    for author in models.Intervention.objects.all():
#        rdf.discover_intervention_links(author)
#    return http.HttpResponse("Done!")
