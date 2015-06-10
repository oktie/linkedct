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

import urllib
import os
import time
import sys

sys.path.append(os.pardir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings
from linkedct import operations, models

import profile

CONFIG = settings.CONFIG

urls = ['start']

#urls = models.Url.objects.filter(status='submitted')
#trial_url = urls[0]
#trial_url.status = 'submitted'
#trial_url.save()

#profile.run("operations.process_xml(trial_url.url, 10000*1024, '127.0.0.1', 'utf-8', True)")
profile.run("operations.process_xml('http://clinicaltrials.gov/show/NCT00003553?displayxml=true', 10000*1024, '127.0.0.1', 'utf-8', True)")
#trial_url.status = 'done'
#trial_url.save()
#print 'Done with ' + trial_url.url
