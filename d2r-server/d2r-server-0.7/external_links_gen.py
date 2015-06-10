

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

for object1 in objectlist:
    print 'map:' +object1+ '__interlinks a d2rq:PropertyBridge;'
    print TAB + 'd2rq:belongsToClassMap map:' +object1+ ';'
    print TAB + 'd2rq:property linkedct:has_external_linkage;'
    print TAB + 'd2rq:refersToClassMap map:external_linkage;'
    print TAB + 'd2rq:join "linkedct_' +object1+ '.slug = linkedct_' +object1+ '_interlinks.' +object1+ '_id";'
    print TAB + 'd2rq:join "linkedct_' +object1+ '_interlinks.external_linkage_id = linkedct_external_linkage.slug";'
    print TAB + '.'
    print 'map:' +object1+ '__seeAlso a d2rq:PropertyBridge;'
    print TAB + 'd2rq:belongsToClassMap map:' +object1+ ';'
    print TAB + 'd2rq:property rdfs:seeAlso;'
    print TAB + 'd2rq:uriColumn "linkedct_external_resource.source_url";'
    print TAB + 'd2rq:condition "linkedct_' +object1+ '.slug = linkedct_' +object1+ '_interlinks.' +object1+ '_id";'
    print TAB + 'd2rq:condition "linkedct_' +object1+ '_interlinks.external_linkage_id = linkedct_external_linkage.slug";'
    print TAB + 'd2rq:condition "linkedct_external_linkage.to_resource_id = linkedct_external_resource.slug";'
    print TAB + '.'