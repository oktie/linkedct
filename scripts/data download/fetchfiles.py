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

#location = "c:\\ctdata\\" 
location = ""

inputfilename = location + "filelist.txt"

infile = open(inputfilename,"r")

for line in infile:
    uri = "http://clinicaltrials.gov" + line.strip() + "?displayxml=true"
    trialid = line.strip()[10:]
    xmlfile = urllib.urlopen(uri)

    outfilename = location + "data" + os.path.sep + trialid + ".xml"
    outfile = open(outfilename,"w")
    outfile.writelines(xmlfile.readlines())
    outfile.close()
