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

location = "c:\\ctdata\\"

inputfilename = location + "xmlfilelist.txt"

infile = open(inputfilename,"r")

outfilename = location + "trials.del"
outfile = open(outfilename,"w")

for line in infile:
    xmlfile=line.strip()
    outline = '"' + xmlfile[:-4] + '"' + ",<XDS FIL='" + xmlfile + "' />\n"
    outfile.write(outline)


outfile.close()
