

list = [('keyword','keyword'),('condition','condition'),('location','location'),
        ('link','link'),('results_reference','reference'), ('arm_group','arm_group'),
        ('location_countries','country'), ('intervention','intervention'), ('secondary_outcome','outcome'),
        ('reference','reference'), ('primary_outcome','outcome'), ('removed_countries','country'), 
        ('overall_official','overall_official')]
TAB = '    '

object1 = 'trial'
for object2, entity2 in list:
    print 'map:'+object1+'__'+object2+'s a d2rq:PropertyBridge;' 
    print TAB + 'd2rq:belongsToClassMap map:'+object1+';'
    print TAB + 'd2rq:property linkedct:'+object1+'_'+object2+';'
    print TAB + 'd2rq:propertyDefinitionLabel "'+object1.capitalize().replace('_',' ')+'\'s '+object2.capitalize().replace('_',' ')+'";'
    print TAB + 'd2rq:refersToClassMap map:'+entity2+';'
    print TAB + 'd2rq:join "linkedct_'+object1+'.slug = linkedct_'+object1+'_'+object2+'s.'+object1+'_id";'
    print TAB + 'd2rq:join "linkedct_'+object1+'_'+object2+'s.'+entity2+'_id = linkedct_'+entity2+'.slug";'
    print TAB + '.'