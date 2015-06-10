

objectlist = [ 'address', 'arm_group', 'city',
               'condition', 'condition_browse', 'contact',
               'country', 'eligibility', 'facility', 
               'intervention', 'intervention_browse', 
               'investigator', 'keyword', 'link',
                'location', 'mesh_term',  'outcome', 
                'overall_official', 'oversight_info', 'reference', 
                'responsible_party', 'sponsor','sponsor_group', 
                'state', 
               #'trial', 'linkage_method', 'external_linkage'
               ]

TAB = '    '

object2 = 'provenance'
entity2 = 'provenance'
for object1 in objectlist:
    print 'map:'+object1+'__'+object2+'s a d2rq:PropertyBridge;' 
    print TAB + 'd2rq:belongsToClassMap map:'+object1+';'
    print TAB + 'd2rq:property linkedct:object_'+object2+';'
#    print TAB + 'd2rq:propertyDefinitionLabel "'+object1.capitalize().replace('_',' ')+'\'s '+object2.capitalize().replace('_',' ')+'";'
    print TAB + 'd2rq:refersToClassMap map:'+entity2+';'
    print TAB + 'd2rq:join "linkedct_'+object1+'.slug = linkedct_'+object1+'_'+object2+'s.'+object1+'_id";'
    print TAB + 'd2rq:join "linkedct_'+object1+'_'+object2+'s.'+entity2+'_id = linkedct_'+entity2+'.slug";'
    print TAB + '.'