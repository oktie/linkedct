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

import os
import sys

sys.path.append(os.pardir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings
from linkedct import operations, models

CONFIG = settings.CONFIG


urls = models.Url.objects.filter(status='inprocess')
while len(urls)>0:
    url_list = urls[:25]
    for trial_url in url_list:
        if trial_url.status=='inprocess':
            trial_url.status = 'submitted'
            trial_url.save()
    for trial_url in url_list:
        if trial_url.status=='submitted':
            trial_url.status = 'inprocess_again'
            trial_url.save()
            #uri = 'http://data.linkedct.org:8081/processxml/' + trial_url + '/'
            #uri = 'http://newyork.isl.sandbox/linkedct/processxml/' + trial_url.url + '/'
            #uri = 'http://localhost:8081/processxml/' + trial_url.url + '/'
            try:
                operations.process_xml(trial_url.url, 10000*1024, '127.0.0.1', 'utf-8', True)
                trial_url.status = 'done'
                trial_url.save()
                print 'Done with ' + trial_url.url
            except:
                trial_url.status = 'error'
                trial_url.save()
                print 'Error in URL: ' + trial_url.url
    urls = models.Url.objects.filter(status='inprocess')
    
urls = models.Url.objects.filter(status='inprocess_again')
while len(urls)>0:
    url_list = urls[:25]
    for trial_url in url_list:
        if trial_url.status=='inprocess_again':
            trial_url.status = 'submitted'
            trial_url.save()
    for trial_url in url_list:
        if trial_url.status=='submitted':
            trial_url.status = 'inprocess'
            trial_url.save()
            #uri = 'http://data.linkedct.org:8081/processxml/' + trial_url + '/'
            #uri = 'http://newyork.isl.sandbox/linkedct/processxml/' + trial_url.url + '/'
            #uri = 'http://localhost:8081/processxml/' + trial_url.url + '/'
            try:
                operations.process_xml(trial_url.url, 10000*1024, '127.0.0.1', 'utf-8', True)
                trial_url.status = 'done'
                trial_url.save()
                print 'Done with ' + trial_url.url
            except:
                trial_url.status = 'error'
                trial_url.save()
                print 'Error in URL: ' + trial_url.url
    urls = models.Url.objects.filter(status='inprocess')


urls = models.Url.objects.filter(status='error')
if len(urls)>0:
    url_list = urls
    for trial_url in url_list:
        if trial_url.status=='error':
            trial_url.status = 'submitted'
            trial_url.save()
    for trial_url in url_list:
        if trial_url.status=='submitted':
            trial_url.status = 'inprocess'
            trial_url.save()
            #uri = 'http://data.linkedct.org:8081/processxml/' + trial_url + '/'
            #uri = 'http://newyork.isl.sandbox/linkedct/processxml/' + trial_url.url + '/'
            #uri = 'http://localhost:8081/processxml/' + trial_url.url + '/'
            try:
                operations.process_xml(trial_url.url, 10000*1024, '127.0.0.1', 'utf-8', True)
                trial_url.status = 'done'
                trial_url.save()
                print 'Done with ' + trial_url.url
            except:
                trial_url.status = 'error'
                trial_url.save()
                print 'Error in URL: ' + trial_url.url
    #urls = models.Url.objects.filter(status='error')