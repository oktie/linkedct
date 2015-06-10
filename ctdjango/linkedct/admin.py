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

from django.contrib import admin
from models import *
import databrowse

# Setting search fields for the admin interface for Author
# NOTE: Remove @ before field names if you are using a DBMS other than MySQL
class TrialAdmin(admin.ModelAdmin):
    search_fields = ['@label', 'trialid','@brief_title']

# Setting search fields for the admin interface for Common entities
class CommonAdmin(admin.ModelAdmin):
    search_fields = ['@label', 'slug']

# Setting search fields for the admin interface for Link entities
class CommonLinkAdmin(admin.ModelAdmin):
    search_fields = ['url']

admin.site.register(Trial, TrialAdmin)

admin.site.register(Provenance, CommonAdmin)

admin.site.register(Linkage_method)
admin.site.register(External_resource, CommonAdmin)
admin.site.register(Alt_name, CommonAdmin)
admin.site.register(Linkage, CommonAdmin)
admin.site.register(External_linkage, CommonAdmin)

admin.site.register(Reference, CommonAdmin)
admin.site.register(Mesh_term, CommonAdmin)
admin.site.register(Condition_browse, CommonAdmin)
admin.site.register(Intervention_browse, CommonAdmin)
admin.site.register(Link, CommonAdmin)
admin.site.register(State, CommonAdmin)
admin.site.register(Investigator, CommonAdmin)
admin.site.register(Responsible_party, CommonAdmin)
admin.site.register(Outcome, CommonAdmin)
admin.site.register(City, CommonAdmin)
admin.site.register(Arm_group, CommonAdmin)
admin.site.register(Intervention, CommonAdmin)
admin.site.register(Contact, CommonAdmin)
admin.site.register(Country, CommonAdmin)
admin.site.register(Address, CommonAdmin)
admin.site.register(Facility, CommonAdmin)
admin.site.register(Location, CommonAdmin)
admin.site.register(Oversight_info, CommonAdmin)
admin.site.register(Eligibility, CommonAdmin)
admin.site.register(Overall_official, CommonAdmin)
admin.site.register(Sponsor, CommonAdmin)
admin.site.register(Sponsor_group, CommonAdmin)
admin.site.register(Condition, CommonAdmin)
admin.site.register(Keyword, CommonAdmin)





# Data browse
# See http://docs.djangoproject.com/en/1.2/ref/contrib/databrowse/
databrowse.site.register(Provenance)
databrowse.site.register(Linkage)
databrowse.site.register(External_linkage)
databrowse.site.register(Linkage_method)
databrowse.site.register(Trial)
databrowse.site.register(Reference)
databrowse.site.register(Mesh_term)
databrowse.site.register(Keyword)
databrowse.site.register(Condition_browse)
databrowse.site.register(Intervention_browse)
databrowse.site.register(Link)
databrowse.site.register(State)
databrowse.site.register(Investigator)
databrowse.site.register(Responsible_party)
databrowse.site.register(Outcome)
databrowse.site.register(City)
databrowse.site.register(Arm_group)
databrowse.site.register(Intervention)
databrowse.site.register(Condition)
databrowse.site.register(Contact)
databrowse.site.register(Country)
databrowse.site.register(Address)
databrowse.site.register(Facility)
databrowse.site.register(Location)
databrowse.site.register(Oversight_info)
databrowse.site.register(Eligibility)
databrowse.site.register(Overall_official)
databrowse.site.register(Sponsor)
databrowse.site.register(Sponsor_group)
