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

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
import re
import hashlib
import htmlentitydefs


# This is used in Django's select_related() function. It helps reduce the
# number of queries performed by doing more JOINs. For more information, see
# http://docs.djangoproject.com/en/dev/ref/models/querysets/#id4
#SELECT_RELATED_LIST = ['journal', 'keyword', 'school', 'series',
                       #'organization', 'book', 'collection', 'inproceedings', ]

class Url(models.Model):
    """ An extra model to store a list of URLs that need processing or are processed """
    url = models.CharField(max_length=128, primary_key=True)
    status = models.CharField(max_length=128, blank=True)
    
    def __unicode__(self):
        return self.url

class CommonInfoBase(models.Model):
    """The base class for most common models, with no provenance.

    This is an abstract class that cannot be instantiated.
    """
    label = models.CharField(max_length=255)
    slug = models.SlugField(max_length=128, primary_key=True)

    class Meta:
        abstract = True
        ## cf: using label as default ordering. can be overriden in sub-classes (cf., e.g., PubEntry)
        #ordering = ['label']

    def __unicode__(self):
        return self.label
    
    def name(self):
        if 'name' in self.__dict__.keys():
            return self.name
        else:
            return self.label

    def save(self, **kwargs):
        """Overwrite Django Model's default save method.

        This is used to auto populate the slug field.
        """
        self.set_slug()
        super(CommonInfoBase, self).save(**kwargs)

    def set_slug(self):
        """Set slug field."""
        if not self.slug:
            self.slug = slugify(self.label)

class Provenance(CommonInfoBase):
    """The Provenance table keeps track of the origin of all data.

    Currently, it only keeps a list of XML's URLs. 
    There should be a many-to-one mapping (foreign key) between each
    object and Provenance for tracking which object is created by which 
    XML file.
    """
    url = models.URLField(verify_exists=False, max_length=512)
    time_updated = models.DateTimeField(auto_now=True)
    time_added = models.DateTimeField(auto_now_add=True)
    ip = models.IPAddressField(null=True)
    encoding = models.CharField(max_length=20, blank=True)
    signature = models.CharField(max_length=33, blank=True)

    def __unicode__(self):
        return self.url

    def save(self, **kwargs):
        """Overwrite Django Model's save method to populate label field."""
        self.label = self.url
        super(Provenance, self).save(**kwargs)

class Alt_name(CommonInfoBase):
    source = models.CharField(max_length=255)
    id = models.CharField(max_length=255)
    altname = models.CharField(max_length=512)

class External_resource(CommonInfoBase):
    #label = models.CharField(max_length=255)
    source_url = models.URLField(verify_exists=False, max_length=2550)
    #oktie: TODO: may need to make this many-to-many in the future
    source_id = models.CharField(max_length=255)
    source_label = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255)
    FORMAT_CHOICES = (
        ('rdf', 'RDF'),
        ('html', 'HTML'),
        ('rdf/html', 'RDF_HTML'),
    )
    source_format = models.CharField(max_length=32, choices=FORMAT_CHOICES)
    
    related_model_name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.label

## Model for storing meta data about linkage methodology
class Linkage_method(CommonInfoBase):
    """Class for Linkage Methodology Met Data."""

    TYPE_CHOICES = (
        ('id-based', 'ID_BASED'),
        ('fuzzy', 'FUZZY_MATCHING'),
        ('exact', 'EXACT_MATCHING'),
        ('semantic', 'SEMANTIC'),
        ('semantic/fuzzy', 'SEMANTIC_FUZZY'),
    )
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.label


class Linkage(CommonInfoBase):
    
    from_object_slug = models.SlugField(max_length=128)
    from_object_type = models.CharField(max_length=128)
    to_object_slug = models.SlugField(max_length=128)
    to_object_type = models.CharField(max_length=128)
    
    method = models.ForeignKey(Linkage_method, related_name='linkage_method_relation')
    
    #def __unicode__(self):
    #    return 'Linkage from \'' + self.from_object_slug + '\' ('+ self.from_object_type + ') ' +\
    #           'to \'' + self.to_object_slug + '\' ('+ self.to_object_type + ')'

class External_linkage(CommonInfoBase):
    
    from_object_slug = models.SlugField(max_length=128)
    from_object_type = models.CharField(max_length=128)
    to_resource = models.ForeignKey(External_resource, related_name='link_to_external_resource')
    
    method = models.ForeignKey(Linkage_method, related_name='linkage_method_link')
    
    score = models.FloatField(null = True)
    
    #def __unicode__(self):
    #    return 'External Linkage from \'' + self.from_object_slug + '\' ('+ self.from_object_type + ') ' +\
    #           'to external resource: ' + self.to_resouce.__unicode__()

class CommonInfo(CommonInfoBase):
    """The base class for most common models.

    This is an abstract class that cannot be instantiated.
    """
    
    # Provenance info for objects
    provenances = models.ManyToManyField(Provenance)
    
    # Boolean info
    is_duplicate = models.BooleanField(default=False)
    is_duplicated_by = models.BooleanField(default=False)
    is_interlinked = models.BooleanField(default=False)
    
    # Disambiguation info for objects
    similars = models.ManyToManyField(Linkage, related_name='%(class)s_similar_to')
    
    # Related info for objects
    relateds = models.ManyToManyField(Linkage, related_name='%(class)s_related_to')
    
    # External links info for objects
    interlinks = models.ManyToManyField(External_linkage, related_name='%(class)s_interlinks_to')
    
    def interlink(self, **kwargs):
        matched_objects = set(External_resource.objects.filter(source_label__iexact=self.label))
        matched_objects = matched_objects.union(set(External_resource.objects.filter(source_label__iexact=self.label.replace(' ','_'))))
        matched_objects = matched_objects.union(set(External_resource.objects.filter(source_label__iexact=slugify(self.label))))
        
        if len(matched_objects)>0 and not self.is_interlinked:
            self.is_interlinked = True
            linkageMethod, created = Linkage_method.objects.get_or_create(
                                type = 'FUZZY_MATCHING',
                                label = 'Standardized String Matching',
                                )
            if created:
                linkageMethod.save()
            for external_resource in matched_objects:
                interlink_hashset = set([self.slug,self._meta.object_name, external_resource.slug, linkageMethod.slug])
                slug = hashlib.md5(str(interlink_hashset)).hexdigest()
                interlink, created = External_linkage.objects.get_or_create(
                                label = slug,
                                from_object_slug = self.slug ,
                                from_object_type = self._meta.object_name,
                                to_resource = external_resource,
                                method = linkageMethod,
                                )
                if created:
                    interlink.save()
                    self.interlinks.add(interlink)
        super(CommonInfoBase, self).save(**kwargs)
            
    class Meta:
        abstract = True




# original: Results_reference_or_reference
class Reference(CommonInfo):
    # property path: /clinical_study/results_reference|/clinical_study/reference/citation/text()
    citation = models.TextField(blank=True)
    # property path: /clinical_study/results_reference|/clinical_study/reference/PMID/text()
    PMID = models.CharField(max_length=255, blank=True)
    
    def interlink(self, **kwargs):
        if self.PMID != '':
            # Create external resource
            label = 'PubMed Article ' + self.PMID + ' (on Bio2RDF)' 
            if len(label)>127:
                        label = hashlib.md5(label).hexdigest()
            external_resource, created = External_resource.objects.get_or_create( 
                            label = label,
                            source_url = 'http://bio2rdf.org/pubmed:'+ self.PMID,
                            source_id = self.PMID,
                            source_label = 'PubMed:' + self.PMID,
                            source_name = 'PubMed on Bio2RDF',
                            source_format = 'RDF_HTML',
                            related_model_name = 'Reference',
                    )
            external_resource.save()
            # link to the external resource
            self.is_interlinked = True
            linkageMethod, created = Linkage_method.objects.get_or_create(
                                type = 'ID_BASED',
                                label = 'Linkage based on known URI pattern',
                                )
            if created:
                linkageMethod.save()
            interlink_hashset = set([self.slug,self._meta.object_name, external_resource.slug, linkageMethod.slug])
            slug = hashlib.md5(str(interlink_hashset)).hexdigest()
            interlink, created = External_linkage.objects.get_or_create(
                            label = slug,
                            from_object_slug = self.slug ,
                            from_object_type = self._meta.object_name,
                            to_resource = external_resource,
                            method = linkageMethod,
                            )
            if created:
                interlink.save()
                self.interlinks.add(interlink)
        super(CommonInfoBase, self).save(**kwargs)
    
    def save(self, **kwargs):
        """Overwrites defauls save method.
        This is used for automatic link discovery.
        """
        self.set_slug()
        super(CommonInfoBase, self).save(**kwargs)
        self.interlink(**kwargs)


class Mesh_term(CommonInfo):

    def save(self, **kwargs):
        """Overwrites defauls save method.
        This is used for automatic link discovery.
        """
        self.set_slug()
        super(CommonInfoBase, self).save(**kwargs)
        self.interlink(**kwargs)


class Condition_browse(CommonInfo):
    # property path: /clinical_study/condition_browse/mesh_term/text()
    mesh_terms = models.ManyToManyField(Mesh_term, null=True, related_name="%(app_label)s_%(class)s_related")

class Intervention_browse(CommonInfo):
    # property path: /clinical_study/intervention_browse/mesh_term/text()
    mesh_terms = models.ManyToManyField(Mesh_term, null=True, related_name="%(app_label)s_%(class)s_related")


class Link(CommonInfo):
    # property path: /clinical_study/link/description/text()
    description = models.CharField(max_length=1023, blank=True)
    # property path: /clinical_study/link/url/text()
    url = models.URLField(blank=True, max_length=511)



class State(CommonInfo):
    # property path: /clinical_study/location/facility/address/state/text()
    state_name = models.CharField(max_length=255, blank=True)



class Investigator(CommonInfo):
    # property path: /clinical_study/location/investigator/last_name/text()
    last_name = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/location/investigator/role/text()
    role = models.CharField(max_length=255, blank=True)



class Responsible_party(CommonInfo):
    # property path: /clinical_study/responsible_party/organization/text()
    organization = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/responsible_party/name_title/text()
    name_title = models.CharField(max_length=255, blank=True)


# original label: Primary_outcome_or_secondary_outcome
class Outcome(CommonInfo):
    # property path: /clinical_study/primary_outcome|/clinical_study/secondary_outcome/safety_issue/text()
    safety_issue = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/primary_outcome|/clinical_study/secondary_outcome/measure/text()
    measure = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/primary_outcome|/clinical_study/secondary_outcome/description/text()
    description = models.TextField(blank=True)
    # property path: /clinical_study/primary_outcome|/clinical_study/secondary_outcome/time_frame/text()
    time_frame = models.CharField(max_length=255, blank=True)



class City(CommonInfo):
    # property path: /clinical_study/location/facility/address/city/text()
    city_name = models.CharField(max_length=255, blank=True)



class Arm_group(CommonInfo):
    # property path: /clinical_study/arm_group/arm_group_label/text()
    arm_group_label = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/arm_group/description/text()
    description = models.TextField(blank=True)
    # property path: /clinical_study/arm_group/arm_group_type/text()
    arm_group_type = models.CharField(max_length=255, blank=True)



class Intervention(CommonInfo):
    # property path: /clinical_study/intervention/arm_group_label/text()
    arm_group_label = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/intervention/description/text()
    description = models.TextField(blank=True)
    # property path: /clinical_study/intervention/other_name/text()
    other_name = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/intervention/intervention_type/text()
    intervention_type = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/intervention/intervention_name/text()
    intervention_name = models.CharField(max_length=255, blank=True)
    
    def interlink(self, **kwargs):
        matched_objects = set(External_resource.objects.filter(source_label__iexact=self.intervention_name))
        matched_objects = matched_objects.union(set(External_resource.objects.filter(source_label__iexact=self.intervention_name.replace(' ','_'))))
        matched_objects = matched_objects.union(set(External_resource.objects.filter(source_label__iexact=slugify(self.intervention_name))))
        
        if len(matched_objects)>0 and not self.is_interlinked:
            self.is_interlinked = True
            linkageMethod, created = Linkage_method.objects.get_or_create(
                                type = 'FUZZY_MATCHING',
                                label = 'Standardized String Matching',
                                )
            if created:
                linkageMethod.save()
            for external_resource in matched_objects:
                interlink_hashset = set([self.slug,self._meta.object_name, external_resource.slug, linkageMethod.slug])
                slug = hashlib.md5(str(interlink_hashset)).hexdigest()
                interlink, created = External_linkage.objects.get_or_create(
                                label = slug,
                                from_object_slug = self.slug ,
                                from_object_type = self._meta.object_name,
                                to_resource = external_resource,
                                method = linkageMethod,
                                )
                if created:
                    interlink.save()
                    self.interlinks.add(interlink)
        super(CommonInfoBase, self).save(**kwargs)
    
    def save(self, **kwargs):
        """Overwrites defauls save method.
        This is used for automatic link discovery.
        """
        self.set_slug()
        super(CommonInfoBase, self).save(**kwargs)
        self.interlink(**kwargs)


# original label: Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact
class Contact(CommonInfo):
    # property path: /clinical_study/overall_contact_backup|/clinical_study/overall_contact|/clinical_study/location/contact_backup|/clinical_study/location/contact/phone_ext/text()
    phone_ext = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/overall_contact_backup|/clinical_study/overall_contact|/clinical_study/location/contact_backup|/clinical_study/location/contact/phone/text()
    phone = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/overall_contact_backup|/clinical_study/overall_contact|/clinical_study/location/contact_backup|/clinical_study/location/contact/email/text()
    email = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/overall_contact_backup|/clinical_study/overall_contact|/clinical_study/location/contact_backup|/clinical_study/location/contact/last_name/text()
    last_name = models.CharField(max_length=255, blank=True)

class Country(CommonInfo):
    # property path: /clinical_study/location/facility/address/country/text()
    country_name = models.CharField(max_length=255, blank=True)

class Address(CommonInfo):
    # property path: /clinical_study/location/facility/address/zip/text()
    zip = models.CharField(max_length=255, blank=True)
    # relation path: /clinical_study/location/facility/address/state
    state = models.ForeignKey(State, null=True, related_name='address__state')
    # relation path: /clinical_study/location/facility/address/country
    country = models.ForeignKey(Country, null=True, related_name='address__country')
    # relation path: /clinical_study/location/facility/address/city
    city = models.ForeignKey(City, null=True, related_name='address__city')
    
    
class Facility(CommonInfo):
    # property path: /clinical_study/location/facility/label/text()
    facility_name = models.CharField(max_length=255, blank=True)
    # relation path: /clinical_study/location/facility/address
    address = models.ForeignKey(Address, null=True, related_name='facility__address')


class Location(CommonInfo):
    # property path: /clinical_study/location/status/text()
    status = models.CharField(max_length=255, blank=True)
    # relation path: /clinical_study/location/facility
    facility = models.ForeignKey(Facility, null=True, related_name="%(app_label)s_%(class)s_related")
    # relation path: /clinical_study/location/investigator
    investigators = models.ManyToManyField(Investigator, null=True, related_name="%(app_label)s_%(class)s_related")
    # relation path: /clinical_study/location/contact_backup
    contact_backups = models.ManyToManyField(Contact, null=True, related_name="%(app_label)s_%(class)s_related1")
    # relation path: /clinical_study/location/contact
    contacts = models.ManyToManyField(Contact, null=True, related_name="%(app_label)s_%(class)s_related2")



class Oversight_info(CommonInfo):
    # property path: /clinical_study/oversight_info/authority/text()
    authority = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/oversight_info/has_dmc/text()
    has_dmc = models.CharField(max_length=255, blank=True)



class Eligibility(CommonInfo):
    # property path: /clinical_study/eligibility/criteria/textblock/text()
    criteria = models.TextField()
    # property path: /clinical_study/eligibility/maximum_age/text()
    maximum_age = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/eligibility/healthy_volunteers/text()
    healthy_volunteers = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/eligibility/study_pop/textblock/text()
    study_pop = models.TextField()
    # property path: /clinical_study/eligibility/minimum_age/text()
    minimum_age = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/eligibility/gender/text()
    gender = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/eligibility/sampling_method/text()
    sampling_method = models.CharField(max_length=255, blank=True)



class Overall_official(CommonInfo):
    # property path: /clinical_study/overall_official/last_name/text()
    last_name = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/overall_official/role/text()
    role = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/overall_official/affiliation/text()
    affiliation = models.CharField(max_length=255, blank=True)


# original label: Collaborator_or_lead_sponsor
class Sponsor(CommonInfo):
    # property path: /clinical_study/sponsors/collaborator|/clinical_study/sponsors/lead_sponsor/agency_class/text()
    agency_class = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/sponsors/collaborator|/clinical_study/sponsors/lead_sponsor/agency/text()
    agency = models.CharField(max_length=255, blank=True)



class Sponsor_group(CommonInfo):
    # relation path: /clinical_study/sponsors/collaborator
    collaborators = models.ManyToManyField(Sponsor, null=True, related_name='%(class)s_collaborator_related')
    # relation path: /clinical_study/sponsors/lead_sponsor
    lead_sponsor = models.ForeignKey(Sponsor, null=True, related_name='%(class)s_lead_sponsor_related')


class Condition(CommonInfo):
    # property path: /clinical_study/condition/text()
    #condition_name = models.CharField(max_length=255, blank=True)
    def save(self, **kwargs):
        """Overwrites defauls save method.
        This is used for automatic link discovery.
        """
        self.set_slug()
        super(CommonInfoBase, self).save(**kwargs)
        self.interlink(**kwargs)

class Keyword(CommonInfo):
    # property path: /clinical_study/keyword/text()
    def save(self, **kwargs):
        """Overwrites defauls save method.
        This is used for automatic link discovery.
        """
        self.set_slug()
        super(CommonInfoBase, self).save(**kwargs)
        self.interlink(**kwargs)

    #keyword = models.CharField(max_length=255, blank=True)
    
class Coordinates(models.Model):
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    address = models.ForeignKey(Address, related_name='coordinates__address')
    
    

class Trial(CommonInfoBase):
    
    #class Meta:
        #verbose_name = 'Trial'
        #ordering = ['-start_date','brief_title']
        
    trialid = models.SlugField(max_length=255)
    lookup_name = models.SlugField(max_length=255)
    
    provenance = models.ForeignKey(Provenance, related_name='%(class)s_provenance_related')
    
    # property path: /clinical_study/lastchanged_date/text()
    lastchanged_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/firstreceived_results_date/text()
    firstreceived_results_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/firstreceived_date/text()
    firstreceived_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/id_info/nct_id/text()
    id_info_nct_id = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/overall_status/text()
    overall_status = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/id_info/secondary_id/text()
    id_info_secondary_id = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/biospec_retention/text()
    biospec_retention = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/required_header/link_text/text()
    required_header_link_text = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/enrollment/text()
    enrollment = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/number_of_arms/text()
    number_of_arms = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/is_section_801/text()
    is_section_801 = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/is_fda_regulated/text()
    is_fda_regulated = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/brief_title/text()
    brief_title = models.CharField(max_length=1023, blank=True)
    # property path: /clinical_study/acronym/text()
    acronym = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/keyword/text()
    #
    # property path: /clinical_study/official_title/text()
    official_title = models.CharField(max_length=1023, blank=True)
    # property path: /clinical_study/study_type/text()
    study_type = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/id_info/nct_alias/text()
    id_info_nct_alias = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/completion_date/text()
    completion_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/verification_date/text()
    verification_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/why_stopped/text()
    why_stopped = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/id_info/org_study_id/text()
    id_info_org_study_id = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/required_header/url/text()
    required_header_url = models.URLField(blank=True)
    # property path: /clinical_study/study_design/text()
    study_design = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/source/text()
    source = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/primary_completion_date/text()
    primary_completion_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/brief_summary/textblock/text()
    brief_summary = models.TextField()
    # property path: /clinical_study/number_of_groups/text()
    number_of_groups = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/required_header/download_date/text()
    required_header_download_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/phase/text()
    phase = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/start_date/text()
    start_date = models.CharField(max_length=255, blank=True)
    # property path: /clinical_study/has_expanded_access/text()
    has_expanded_access = models.CharField(max_length=255, blank=True)

    biospec_descr = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True) 
    
    # property path: /clinical_study/keyword/text()
    keywords = models.ManyToManyField(Keyword, null=True, related_name='%(class)s_keyword_related')
    # property path: /clinical_study/condition/text()
    conditions = models.ManyToManyField(Condition, null=True, related_name="%(class)s_conditions_related")
    # relation path: /clinical_study/location
    locations = models.ManyToManyField(Location, null=True, related_name="%(class)s_locations_related")
    # relation path: /clinical_study/condition_browse
    condition_browse = models.ForeignKey(Condition_browse, null=True, related_name='%(class)s_condition_browse_related')
    # relation path: /clinical_study/intervention_browse
    intervention_browse = models.ForeignKey(Intervention_browse, null=True, related_name='%(class)s_intervention_related')
    # relation path: /clinical_study/link
    links = models.ManyToManyField(Link, null=True, related_name='%(class)s_links_related')
    # relation path: /clinical_study/responsible_party
    responsible_party = models.ForeignKey(Responsible_party, null=True, related_name='clinical_study_responsible_party_related')
    # relation path: /clinical_study/results_reference
    results_references = models.ManyToManyField(Reference, null=True, related_name='%(class)s_results_reference_related')
    # relation path: /clinical_study/overall_contact
    overall_contact = models.ForeignKey(Contact, null=True, related_name='clinical_study__overall_contact')
    # relation path: /clinical_study/arm_group
    arm_groups = models.ManyToManyField(Arm_group, null=True, related_name='%(class)s_arm_group_related')
    # relation path: /clinical_study/location_countries
    location_countries = models.ManyToManyField(Country, null=True, related_name='%(class)s_location_countries_related')
    # relation path: /clinical_study/intervention
    interventions = models.ManyToManyField(Intervention, null=True, related_name='%(class)s_intervention_related')
    # relation path: /clinical_study/secondary_outcome
    secondary_outcomes = models.ManyToManyField(Outcome, null=True, related_name='%(class)s_secondary_outcome_related')
    # relation path: /clinical_study/biospec_descr
    #biospec_descr = models.ForeignKey(Biospec_descr, null=True, related_name='clinical_study__biospec_descr')
    # relation path: /clinical_study/overall_contact_backup
    overall_contact_backup = models.ForeignKey(Contact, null=True, related_name='clinical_study__overall_contact_backup')
    # relation path: /clinical_study/detailed_description
    #detailed_description = models.ForeignKey(Detailed_description, null=True, related_name='clinical_study__detailed_description')
    # relation path: /clinical_study/reference
    references = models.ManyToManyField(Reference, null=True, related_name='%(class)s_reference_related')
    # relation path: /clinical_study/primary_outcome
    primary_outcomes = models.ManyToManyField(Outcome, null=True, related_name='%(class)s_primary_outcome_related')
    # relation path: /clinical_study/sponsors
    sponsor_group = models.ForeignKey(Sponsor_group, null=True, related_name='clinical_study__sponsors')
    # relation path: /clinical_study/oversight_info
    oversight_info = models.ForeignKey(Oversight_info, null=True, related_name='clinical_study__oversight_info')
    # relation path: /clinical_study/removed_countries/country
    removed_countries = models.ManyToManyField(Country, null=True, related_name='%(class)s_removed_countries_related)')
    # relation path: /clinical_study/eligibility
    eligibility = models.ForeignKey(Eligibility, null=True, related_name='clinical_study__eligibility')
    # relation path: /clinical_study/overall_official
    overall_officials = models.ManyToManyField(Overall_official, null=True, related_name='%(class)s_overall_official_related')

    #coordinates = models.ManyToManyField(Coordinates, null=True, related_name='%(class)s_coordinates_related')

#    <!ELEMENT clinical_study (
#          required_header,
#          id_info,
#          brief_title,
#          acronym?,
#          official_title?,
#          sponsors,
#          source,
#          oversight_info?,
#          brief_summary?,
#          detailed_description?,
#          overall_status,
#          why_stopped?,
#          start_date?,
#          completion_date?,
#          primary_completion_date?,
#          phase,
#          study_type,
#          study_design,
#          primary_outcome*,
#          secondary_outcome*,
#          number_of_arms?,
#          number_of_groups?,
#          enrollment?,
#          condition*,
#          arm_group*,
#          intervention*,
#          biospec_retention?,
#          biospec_descr?,
#          eligibility?,
#          overall_official*,
#          overall_contact?,
#          overall_contact_backup?,
#          location*,
#          location_countries?,
#          removed_countries?,
#          link*,
#          reference*,
#          results_reference*,
#          verification_date?,
#          lastchanged_date?,
#          firstreceived_date,
#          firstreceived_results_date?,
#          responsible_party?,
#          keyword*,
#          is_fda_regulated?,
#          is_section_801?,
#          has_expanded_access?,
#          condition_browse?,
#          intervention_browse?)>




