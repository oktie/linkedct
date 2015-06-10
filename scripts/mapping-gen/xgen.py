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

mapfilename  = "/home/user/workspace/linkedct/scripts/mapping-gen/mapping.xml"
mapfile = open (mapfilename, 'r')

uri_prefix = 'http://www.linkedct.org/0.1#'
path_prefix = '/clinical_studies/clinical_study'

TAB = '    '

#from xml.dom import minidom
#url = "http://clinicaltrials.gov/show/NCT00001372?displayxml=true"
#dom = minidom.parse(urllib.urlopen(url))
from elementtree.ElementTree import *
from xml.parsers.expat import ExpatError

pr = parse(mapfile).getroot()

classProperty = {}
classPaths = {}
for entity in pr.findall('entity'):
  className = entity.get('type').replace(uri_prefix,'')
  classPath = entity.get('path').replace(path_prefix,'')
  classPaths[className] = classPath
  classProperty[className] = []
  
  print 'class ' + className.capitalize() + '(CommonInfo):'
  propertyNamePaths = []
  for property in entity.findall('property'):
    propertyName = property.get('name').replace(uri_prefix,'')
    propertyPath = property.get('path')
    propertyKey  = False
    propertyNamePaths.append((propertyName,propertyPath))
    if property.get('key') == 'true':
      propertyKey = True
    
    if propertyName == 'name':
      propertyName = className + '_name'
    
    print TAB + '# property path: ' + propertyPath
    print TAB + propertyName + ' = models.CharField(max_length=255, blank=True)'
  
  classProperty[className] = propertyNamePaths

  for relation in entity.findall('relation'):
    relationName = relation.get('name').replace(uri_prefix,'')
    relationPath = classPath + '/' + relation.get('path')
    relationTargetEntity  = relation.get('targetEntity').replace(uri_prefix,'')
    # TODO: need <lookupkey> child?
    
 
    print TAB + '# relation path: ' + relationPath
    print TAB + relationName + ' = models.ForeignKey(' + relationTargetEntity.capitalize() + ', null=True, related_name=\'' + className + '__' + relationName + '\')'
  
  print
  print
  print

print
print '## Admin registration commands'
print

for className in classProperty.keys():
  print 'admin.site.register(' + className.capitalize() + ', CommonAdmin)'

for className in classProperty.keys():
  print 'databrowse.site.register(' + className.capitalize() + ')'


print
print '## Array of classNames'
print

classArrayString = '['

for className in classProperty.keys():
  classArrayString += className.capitalize() + ', '
classArrayString = classArrayString[:-2] + ']'
print classArrayString

print
print '## code for fetching attributes'
print

TAB = '    '
for className in classProperty.keys():
  print 
  print TAB + TAB + '##'
  print TAB + TAB + '## class: ' + className
  print TAB + TAB + '##'
  print
  print TAB + TAB + className + 's_hashset = set()'
  classPathList = []
  if classPaths[className].find('|') == -1:
    classPathList.append(classPaths[className])
  else:
    for c in classPaths[className].split('|'):
      classPathList.append(c)
  for classPath in classPathList:
   if classPath.startswith('/'):
    print
    print TAB + TAB + className + '_results = p.findall(\''+ classPath[1:] +'\')'
    print TAB + TAB + 'for '+ className +'_result in '+ className +'_results:'
    for (propertyName,propertyPath) in classProperty.get(className):
      print TAB + TAB + TAB + className + '_hashset = set()'
      if propertyName=='name':
	propertyName = className + '_name'
      if propertyPath!='text()':
	print TAB + TAB + TAB + propertyName + ' = \'\''
	print TAB + TAB + TAB + propertyName + '_result = '+ className +'_result.findall(\''+ propertyPath.replace('/text()','') +'\')'
	print TAB + TAB + TAB + 'if ' + propertyName + '_result:'
	print TAB + TAB + TAB + TAB + propertyName + ' = ' + propertyName + '_result[0].text'
	print TAB + TAB + TAB + TAB + className + '_hashset.add(' + propertyName + '_result[0].text)'
      else:
	print TAB + TAB + TAB + 'if ' + className + '_results:'
	print TAB + TAB + TAB + TAB + propertyName + ' = ' + className + '_results[0].text'
	print TAB + TAB + TAB + TAB + className + '_hashset.add(' + className + '_result[0].text)'
    print TAB + TAB + TAB + 'slug = hashlib.md5(str(' + className + '_hashset)).hexdigest()'
    print TAB + TAB + TAB + '#' + className + '_name = ...'
    print TAB + TAB + TAB + className +', created = models.'+ className.capitalize() +'.objects.get_or_create('
    print TAB + TAB + TAB + TAB + TAB + TAB + TAB + '#name = ' + className + '_name,'
    print TAB + TAB + TAB + TAB + TAB + TAB + TAB + 'name = slug,'
    print TAB + TAB + TAB + TAB + TAB + TAB + TAB + 'slug = slug,'
    for (propertyName,propertyPath) in classProperty.get(className):
      if propertyName=='name':
	propertyName = className + '_name'
      print TAB + TAB + TAB + TAB + TAB + TAB + TAB + propertyName +' = '+ propertyName +','
    print TAB + TAB + TAB + TAB + TAB + TAB + TAB + ')'
    print TAB + TAB + TAB + className + '.provenances.add(provenance)'
    print 
    print TAB + TAB + TAB + className + 's_hashset = ' + className + 's_hashset.union(' + className + '_hashset)'
    print TAB + TAB + TAB + className +'.save()'
    print TAB + TAB + TAB + '#trial.'+ className +'s.add(' + className +  ')'


mapfile.close()

