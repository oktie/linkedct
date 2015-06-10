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


class Results_reference_or_reference(CommonInfo):
    # property path: citation/text()
    citation = models.CharField(max_length=255, blank=True)
    # property path: PMID/text()
    PMID = models.CharField(max_length=255, blank=True)



class Mesh_term(CommonInfo):
    # property path: text()
    mesh_term = models.CharField(max_length=255, blank=True)



class Condition_browse(CommonInfo):
    # relation path: /condition_browse/mesh_term
    mesh_term = models.ForeignKey(Mesh_term, null=True, related_name='condition_browse__mesh_term')



class Intervention_browse(CommonInfo):
    # property path: mesh_term/text()
    mesh_term = models.CharField(max_length=255, blank=True)



class Link(CommonInfo):
    # property path: description/text()
    description = models.CharField(max_length=255, blank=True)
    # property path: url/text()
    url = models.CharField(max_length=255, blank=True)



class State(CommonInfo):
    # property path: text()
    state_name = models.CharField(max_length=255, blank=True)



class Investigator(CommonInfo):
    # property path: last_name/text()
    last_name = models.CharField(max_length=255, blank=True)
    # property path: role/text()
    role = models.CharField(max_length=255, blank=True)



class Responsible_party(CommonInfo):
    # property path: organization/text()
    organization = models.CharField(max_length=255, blank=True)
    # property path: name_title/text()
    name_title = models.CharField(max_length=255, blank=True)



class Primary_outcome_or_secondary_outcome(CommonInfo):
    # property path: safety_issue/text()
    safety_issue = models.CharField(max_length=255, blank=True)
    # property path: measure/text()
    measure = models.CharField(max_length=255, blank=True)
    # property path: description/text()
    description = models.CharField(max_length=255, blank=True)
    # property path: time_frame/text()
    time_frame = models.CharField(max_length=255, blank=True)



class City(CommonInfo):
    # property path: text()
    city_name = models.CharField(max_length=255, blank=True)



class Arm_group(CommonInfo):
    # property path: arm_group_label/text()
    arm_group_label = models.CharField(max_length=255, blank=True)
    # property path: description/text()
    description = models.CharField(max_length=255, blank=True)
    # property path: arm_group_type/text()
    arm_group_type = models.CharField(max_length=255, blank=True)



class Intervention(CommonInfo):
    # property path: arm_group_label/text()
    arm_group_label = models.CharField(max_length=255, blank=True)
    # property path: description/text()
    description = models.CharField(max_length=255, blank=True)
    # property path: other_name/text()
    other_name = models.CharField(max_length=255, blank=True)
    # property path: intervention_type/text()
    intervention_type = models.CharField(max_length=255, blank=True)
    # property path: intervention_name/text()
    intervention_name = models.CharField(max_length=255, blank=True)



class Biospec_descr(CommonInfo):
    # property path: textblock/text()
    textblock = models.CharField(max_length=255, blank=True)



class Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact(CommonInfo):
    # property path: phone_ext/text()
    phone_ext = models.CharField(max_length=255, blank=True)
    # property path: phone/text()
    phone = models.CharField(max_length=255, blank=True)
    # property path: email/text()
    email = models.CharField(max_length=255, blank=True)
    # property path: last_name/text()
    last_name = models.CharField(max_length=255, blank=True)



class Detailed_description(CommonInfo):
    # property path: textblock/text()
    textblock = models.CharField(max_length=255, blank=True)



class Country(CommonInfo):
    # property path: text()
    country_name = models.CharField(max_length=255, blank=True)



class Location_countries(CommonInfo):
    # relation path: /location_countries/country
    country = models.ForeignKey(Country, null=True, related_name='location_countries__country')



class Address(CommonInfo):
    # property path: zip/text()
    zip = models.CharField(max_length=255, blank=True)
    # relation path: /location/facility/address/state
    state = models.ForeignKey(State, null=True, related_name='address__state')
    # relation path: /location/facility/address/country
    country = models.ForeignKey(Country, null=True, related_name='address__country')
    # relation path: /location/facility/address/city
    city = models.ForeignKey(City, null=True, related_name='address__city')



class Facility(CommonInfo):
    # property path: name/text()
    facility_name = models.CharField(max_length=255, blank=True)
    # relation path: /location/facility/address
    address = models.ForeignKey(Address, null=True, related_name='facility__address')



class Location(CommonInfo):
    # property path: status/text()
    status = models.CharField(max_length=255, blank=True)
    # relation path: /location/facility
    facility = models.ForeignKey(Facility, null=True, related_name='location__facility')
    # relation path: /location/investigator
    investigator = models.ForeignKey(Investigator, null=True, related_name='location__investigator')
    # relation path: /location/contact_backup
    contact_backup = models.ForeignKey(Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, null=True, related_name='location__contact_backup')
    # relation path: /location/contact
    contact = models.ForeignKey(Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, null=True, related_name='location__contact')



class Oversight_info(CommonInfo):
    # property path: authority/text()
    authority = models.CharField(max_length=255, blank=True)
    # property path: has_dmc/text()
    has_dmc = models.CharField(max_length=255, blank=True)



class Eligibility(CommonInfo):
    # property path: criteria/textblock/text()
    criteria_textblock = models.CharField(max_length=255, blank=True)
    # property path: maximum_age/text()
    maximum_age = models.CharField(max_length=255, blank=True)
    # property path: healthy_volunteers/text()
    healthy_volunteers = models.CharField(max_length=255, blank=True)
    # property path: study_pop/textblock/text()
    study_pop_textblock = models.CharField(max_length=255, blank=True)
    # property path: minimum_age/text()
    minimum_age = models.CharField(max_length=255, blank=True)
    # property path: gender/text()
    gender = models.CharField(max_length=255, blank=True)
    # property path: sampling_method/text()
    sampling_method = models.CharField(max_length=255, blank=True)



class Overall_official(CommonInfo):
    # property path: last_name/text()
    last_name = models.CharField(max_length=255, blank=True)
    # property path: role/text()
    role = models.CharField(max_length=255, blank=True)
    # property path: affiliation/text()
    affiliation = models.CharField(max_length=255, blank=True)



class Collaborator_or_lead_sponsor(CommonInfo):
    # property path: agency_class/text()
    agency_class = models.CharField(max_length=255, blank=True)
    # property path: agency/text()
    agency = models.CharField(max_length=255, blank=True)



class Sponsors(CommonInfo):
    # relation path: /sponsors/collaborator
    collaborator = models.ForeignKey(Collaborator_or_lead_sponsor, null=True, related_name='sponsors__collaborator')
    # relation path: /sponsors/lead_sponsor
    lead_sponsor = models.ForeignKey(Collaborator_or_lead_sponsor, null=True, related_name='sponsors__lead_sponsor')



class Clinical_study(CommonInfo):
    # property path: lastchanged_date/text()
    lastchanged_date = models.CharField(max_length=255, blank=True)
    # property path: firstreceived_results_date/text()
    firstreceived_results_date = models.CharField(max_length=255, blank=True)
    # property path: firstreceived_date/text()
    firstreceived_date = models.CharField(max_length=255, blank=True)
    # property path: id_info/nct_id/text()
    id_info_nct_id = models.CharField(max_length=255, blank=True)
    # property path: overall_status/text()
    overall_status = models.CharField(max_length=255, blank=True)
    # property path: id_info/secondary_id/text()
    id_info_secondary_id = models.CharField(max_length=255, blank=True)
    # property path: biospec_retention/text()
    biospec_retention = models.CharField(max_length=255, blank=True)
    # property path: required_header/link_text/text()
    required_header_link_text = models.CharField(max_length=255, blank=True)
    # property path: enrollment/text()
    enrollment = models.CharField(max_length=255, blank=True)
    # property path: number_of_arms/text()
    number_of_arms = models.CharField(max_length=255, blank=True)
    # property path: is_section_801/text()
    is_section_801 = models.CharField(max_length=255, blank=True)
    # property path: is_fda_regulated/text()
    is_fda_regulated = models.CharField(max_length=255, blank=True)
    # property path: brief_title/text()
    brief_title = models.CharField(max_length=255, blank=True)
    # property path: acronym/text()
    acronym = models.CharField(max_length=255, blank=True)
    # property path: condition/text()
    condition = models.CharField(max_length=255, blank=True)
    # property path: keyword/text()
    keyword = models.CharField(max_length=255, blank=True)
    # property path: official_title/text()
    official_title = models.CharField(max_length=255, blank=True)
    # property path: study_type/text()
    study_type = models.CharField(max_length=255, blank=True)
    # property path: id_info/nct_alias/text()
    id_info_nct_alias = models.CharField(max_length=255, blank=True)
    # property path: completion_date/text()
    completion_date = models.CharField(max_length=255, blank=True)
    # property path: verification_date/text()
    verification_date = models.CharField(max_length=255, blank=True)
    # property path: why_stopped/text()
    why_stopped = models.CharField(max_length=255, blank=True)
    # property path: id_info/org_study_id/text()
    id_info_org_study_id = models.CharField(max_length=255, blank=True)
    # property path: required_header/url/text()
    required_header_url = models.CharField(max_length=255, blank=True)
    # property path: study_design/text()
    study_design = models.CharField(max_length=255, blank=True)
    # property path: source/text()
    source = models.CharField(max_length=255, blank=True)
    # property path: primary_completion_date/text()
    primary_completion_date = models.CharField(max_length=255, blank=True)
    # property path: brief_summary/textblock/text()
    brief_summary_textblock = models.CharField(max_length=255, blank=True)
    # property path: number_of_groups/text()
    number_of_groups = models.CharField(max_length=255, blank=True)
    # property path: required_header/download_date/text()
    required_header_download_date = models.CharField(max_length=255, blank=True)
    # property path: phase/text()
    phase = models.CharField(max_length=255, blank=True)
    # property path: start_date/text()
    start_date = models.CharField(max_length=255, blank=True)
    # property path: has_expanded_access/text()
    has_expanded_access = models.CharField(max_length=255, blank=True)
    # relation path: /location
    location = models.ForeignKey(Location, null=True, related_name='clinical_study__location')
    # relation path: /condition_browse
    condition_browse = models.ForeignKey(Condition_browse, null=True, related_name='clinical_study__condition_browse')
    # relation path: /intervention_browse
    intervention_browse = models.ForeignKey(Intervention_browse, null=True, related_name='clinical_study__intervention_browse')
    # relation path: /link
    link = models.ForeignKey(Link, null=True, related_name='clinical_study__link')
    # relation path: /responsible_party
    responsible_party = models.ForeignKey(Responsible_party, null=True, related_name='clinical_study__responsible_party')
    # relation path: /results_reference
    results_reference = models.ForeignKey(Results_reference_or_reference, null=True, related_name='clinical_study__results_reference')
    # relation path: /overall_contact
    overall_contact = models.ForeignKey(Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, null=True, related_name='clinical_study__overall_contact')
    # relation path: /arm_group
    arm_group = models.ForeignKey(Arm_group, null=True, related_name='clinical_study__arm_group')
    # relation path: /location_countries
    location_countries = models.ForeignKey(Location_countries, null=True, related_name='clinical_study__location_countries')
    # relation path: /intervention
    intervention = models.ForeignKey(Intervention, null=True, related_name='clinical_study__intervention')
    # relation path: /secondary_outcome
    secondary_outcome = models.ForeignKey(Primary_outcome_or_secondary_outcome, null=True, related_name='clinical_study__secondary_outcome')
    # relation path: /biospec_descr
    biospec_descr = models.ForeignKey(Biospec_descr, null=True, related_name='clinical_study__biospec_descr')
    # relation path: /overall_contact_backup
    overall_contact_backup = models.ForeignKey(Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, null=True, related_name='clinical_study__overall_contact_backup')
    # relation path: /detailed_description
    detailed_description = models.ForeignKey(Detailed_description, null=True, related_name='clinical_study__detailed_description')
    # relation path: /reference
    reference = models.ForeignKey(Results_reference_or_reference, null=True, related_name='clinical_study__reference')
    # relation path: /primary_outcome
    primary_outcome = models.ForeignKey(Primary_outcome_or_secondary_outcome, null=True, related_name='clinical_study__primary_outcome')
    # relation path: /sponsors
    sponsors = models.ForeignKey(Sponsors, null=True, related_name='clinical_study__sponsors')
    # relation path: /oversight_info
    oversight_info = models.ForeignKey(Oversight_info, null=True, related_name='clinical_study__oversight_info')
    # relation path: /removed_countries/country
    removed_countries_country = models.ForeignKey(Country, null=True, related_name='clinical_study__removed_countries_country')
    # relation path: /eligibility
    eligibility = models.ForeignKey(Eligibility, null=True, related_name='clinical_study__eligibility')
    # relation path: /overall_official
    overall_official = models.ForeignKey(Overall_official, null=True, related_name='clinical_study__overall_official')




## Admin registration commands

admin.site.register(Primary_outcome_or_secondary_outcome, CommonAdmin)
admin.site.register(Facility, CommonAdmin)
admin.site.register(Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, CommonAdmin)
admin.site.register(Responsible_party, CommonAdmin)
admin.site.register(Detailed_description, CommonAdmin)
admin.site.register(Intervention, CommonAdmin)
admin.site.register(City, CommonAdmin)
admin.site.register(Clinical_study, CommonAdmin)
admin.site.register(Results_reference_or_reference, CommonAdmin)
admin.site.register(State, CommonAdmin)
admin.site.register(Location, CommonAdmin)
admin.site.register(Collaborator_or_lead_sponsor, CommonAdmin)
admin.site.register(Eligibility, CommonAdmin)
admin.site.register(Arm_group, CommonAdmin)
admin.site.register(Sponsors, CommonAdmin)
admin.site.register(Overall_official, CommonAdmin)
admin.site.register(Biospec_descr, CommonAdmin)
admin.site.register(Address, CommonAdmin)
admin.site.register(Mesh_term, CommonAdmin)
admin.site.register(Location_countries, CommonAdmin)
admin.site.register(Investigator, CommonAdmin)
admin.site.register(Country, CommonAdmin)
admin.site.register(Oversight_info, CommonAdmin)
admin.site.register(Intervention_browse, CommonAdmin)
admin.site.register(Link, CommonAdmin)
admin.site.register(Condition_browse, CommonAdmin)
databrowse.site.register(Primary_outcome_or_secondary_outcome)
databrowse.site.register(Facility)
databrowse.site.register(Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact)
databrowse.site.register(Responsible_party)
databrowse.site.register(Detailed_description)
databrowse.site.register(Intervention)
databrowse.site.register(City)
databrowse.site.register(Clinical_study)
databrowse.site.register(Results_reference_or_reference)
databrowse.site.register(State)
databrowse.site.register(Location)
databrowse.site.register(Collaborator_or_lead_sponsor)
databrowse.site.register(Eligibility)
databrowse.site.register(Arm_group)
databrowse.site.register(Sponsors)
databrowse.site.register(Overall_official)
databrowse.site.register(Biospec_descr)
databrowse.site.register(Address)
databrowse.site.register(Mesh_term)
databrowse.site.register(Location_countries)
databrowse.site.register(Investigator)
databrowse.site.register(Country)
databrowse.site.register(Oversight_info)
databrowse.site.register(Intervention_browse)
databrowse.site.register(Link)
databrowse.site.register(Condition_browse)

## Array of classNames

[Primary_outcome_or_secondary_outcome, Facility, Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, Responsible_party, Detailed_description, Intervention, City, Clinical_study, Results_reference_or_reference, State, Location, Collaborator_or_lead_sponsor, Eligibility, Arm_group, Sponsors, Overall_official, Biospec_descr, Address, Mesh_term, Location_countries, Investigator, Country, Oversight_info, Intervention_browse, Link, Condition_browse]

## code for fetching attributes


        ##
        ## class: primary_outcome_or_secondary_outcome
        ##

        primary_outcome_or_secondary_outcomes_hashset = set()

        primary_outcome_or_secondary_outcome_results = p.findall('primary_outcome')
        for primary_outcome_or_secondary_outcome_result in primary_outcome_or_secondary_outcome_results:
            primary_outcome_or_secondary_outcome_hashset = set()
            safety_issue = ''
            safety_issue_result = primary_outcome_or_secondary_outcome_result.findall('safety_issue')
            if safety_issue_result:
                safety_issue = safety_issue_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(safety_issue_result[0].text)
            primary_outcome_or_secondary_outcome_hashset = set()
            measure = ''
            measure_result = primary_outcome_or_secondary_outcome_result.findall('measure')
            if measure_result:
                measure = measure_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(measure_result[0].text)
            primary_outcome_or_secondary_outcome_hashset = set()
            description = ''
            description_result = primary_outcome_or_secondary_outcome_result.findall('description')
            if description_result:
                description = description_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(description_result[0].text)
            primary_outcome_or_secondary_outcome_hashset = set()
            time_frame = ''
            time_frame_result = primary_outcome_or_secondary_outcome_result.findall('time_frame')
            if time_frame_result:
                time_frame = time_frame_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(time_frame_result[0].text)
            slug = hashlib.md5(str(primary_outcome_or_secondary_outcome_hashset)).hexdigest()
            #primary_outcome_or_secondary_outcome_name = ...
            primary_outcome_or_secondary_outcome, created = models.Primary_outcome_or_secondary_outcome.objects.get_or_create(
                            #name = primary_outcome_or_secondary_outcome_name,
                            name = slug,
                            slug = slug,
                            safety_issue = safety_issue,
                            measure = measure,
                            description = description,
                            time_frame = time_frame,
                            )
            primary_outcome_or_secondary_outcome.provenances.add(provenance)

            primary_outcome_or_secondary_outcomes_hashset = primary_outcome_or_secondary_outcomes_hashset.union(primary_outcome_or_secondary_outcome_hashset)
            primary_outcome_or_secondary_outcome.save()
            #trial.primary_outcome_or_secondary_outcomes.add(primary_outcome_or_secondary_outcome)

        primary_outcome_or_secondary_outcome_results = p.findall('secondary_outcome')
        for primary_outcome_or_secondary_outcome_result in primary_outcome_or_secondary_outcome_results:
            primary_outcome_or_secondary_outcome_hashset = set()
            safety_issue = ''
            safety_issue_result = primary_outcome_or_secondary_outcome_result.findall('safety_issue')
            if safety_issue_result:
                safety_issue = safety_issue_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(safety_issue_result[0].text)
            primary_outcome_or_secondary_outcome_hashset = set()
            measure = ''
            measure_result = primary_outcome_or_secondary_outcome_result.findall('measure')
            if measure_result:
                measure = measure_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(measure_result[0].text)
            primary_outcome_or_secondary_outcome_hashset = set()
            description = ''
            description_result = primary_outcome_or_secondary_outcome_result.findall('description')
            if description_result:
                description = description_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(description_result[0].text)
            primary_outcome_or_secondary_outcome_hashset = set()
            time_frame = ''
            time_frame_result = primary_outcome_or_secondary_outcome_result.findall('time_frame')
            if time_frame_result:
                time_frame = time_frame_result[0].text
                primary_outcome_or_secondary_outcome_hashset.add(time_frame_result[0].text)
            slug = hashlib.md5(str(primary_outcome_or_secondary_outcome_hashset)).hexdigest()
            #primary_outcome_or_secondary_outcome_name = ...
            primary_outcome_or_secondary_outcome, created = models.Primary_outcome_or_secondary_outcome.objects.get_or_create(
                            #name = primary_outcome_or_secondary_outcome_name,
                            name = slug,
                            slug = slug,
                            safety_issue = safety_issue,
                            measure = measure,
                            description = description,
                            time_frame = time_frame,
                            )
            primary_outcome_or_secondary_outcome.provenances.add(provenance)

            primary_outcome_or_secondary_outcomes_hashset = primary_outcome_or_secondary_outcomes_hashset.union(primary_outcome_or_secondary_outcome_hashset)
            primary_outcome_or_secondary_outcome.save()
            #trial.primary_outcome_or_secondary_outcomes.add(primary_outcome_or_secondary_outcome)

        ##
        ## class: facility
        ##

        facilitys_hashset = set()

        facility_results = p.findall('location/facility')
        for facility_result in facility_results:
            facility_hashset = set()
            facility_name = ''
            facility_name_result = facility_result.findall('name')
            if facility_name_result:
                facility_name = facility_name_result[0].text
                facility_hashset.add(facility_name_result[0].text)
            slug = hashlib.md5(str(facility_hashset)).hexdigest()
            #facility_name = ...
            facility, created = models.Facility.objects.get_or_create(
                            #name = facility_name,
                            name = slug,
                            slug = slug,
                            facility_name = facility_name,
                            )
            facility.provenances.add(provenance)

            facilitys_hashset = facilitys_hashset.union(facility_hashset)
            facility.save()
            #trial.facilitys.add(facility)

        ##
        ## class: overall_contact_backup_or_overall_contact_or_contact_backup_or_contact
        ##

        overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset = set()

        overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results = p.findall('overall_contact_backup')
        for overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result in overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results:
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone_ext = ''
            phone_ext_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone_ext')
            if phone_ext_result:
                phone_ext = phone_ext_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_ext_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone = ''
            phone_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone')
            if phone_result:
                phone = phone_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            email = ''
            email_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('email')
            if email_result:
                email = email_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(email_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            last_name = ''
            last_name_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(last_name_result[0].text)
            slug = hashlib.md5(str(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)).hexdigest()
            #overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name = ...
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, created = models.Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.objects.get_or_create(
                            #name = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name,
                            name = slug,
                            slug = slug,
                            phone_ext = phone_ext,
                            phone = phone,
                            email = email,
                            last_name = last_name,
                            )
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.provenances.add(provenance)

            overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset = overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset.union(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.save()
            #trial.overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts.add(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact)

        overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results = p.findall('overall_contact')
        for overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result in overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results:
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone_ext = ''
            phone_ext_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone_ext')
            if phone_ext_result:
                phone_ext = phone_ext_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_ext_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone = ''
            phone_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone')
            if phone_result:
                phone = phone_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            email = ''
            email_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('email')
            if email_result:
                email = email_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(email_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            last_name = ''
            last_name_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(last_name_result[0].text)
            slug = hashlib.md5(str(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)).hexdigest()
            #overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name = ...
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, created = models.Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.objects.get_or_create(
                            #name = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name,
                            name = slug,
                            slug = slug,
                            phone_ext = phone_ext,
                            phone = phone,
                            email = email,
                            last_name = last_name,
                            )
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.provenances.add(provenance)

            overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset = overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset.union(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.save()
            #trial.overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts.add(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact)

        overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results = p.findall('location/contact_backup')
        for overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result in overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results:
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone_ext = ''
            phone_ext_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone_ext')
            if phone_ext_result:
                phone_ext = phone_ext_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_ext_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone = ''
            phone_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone')
            if phone_result:
                phone = phone_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            email = ''
            email_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('email')
            if email_result:
                email = email_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(email_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            last_name = ''
            last_name_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(last_name_result[0].text)
            slug = hashlib.md5(str(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)).hexdigest()
            #overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name = ...
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, created = models.Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.objects.get_or_create(
                            #name = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name,
                            name = slug,
                            slug = slug,
                            phone_ext = phone_ext,
                            phone = phone,
                            email = email,
                            last_name = last_name,
                            )
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.provenances.add(provenance)

            overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset = overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset.union(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.save()
            #trial.overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts.add(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact)

        overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results = p.findall('location/contact')
        for overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result in overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_results:
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone_ext = ''
            phone_ext_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone_ext')
            if phone_ext_result:
                phone_ext = phone_ext_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_ext_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            phone = ''
            phone_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('phone')
            if phone_result:
                phone = phone_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(phone_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            email = ''
            email_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('email')
            if email_result:
                email = email_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(email_result[0].text)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset = set()
            last_name = ''
            last_name_result = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset.add(last_name_result[0].text)
            slug = hashlib.md5(str(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)).hexdigest()
            #overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name = ...
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact, created = models.Overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.objects.get_or_create(
                            #name = overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_name,
                            name = slug,
                            slug = slug,
                            phone_ext = phone_ext,
                            phone = phone,
                            email = email,
                            last_name = last_name,
                            )
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.provenances.add(provenance)

            overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset = overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts_hashset.union(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact_hashset)
            overall_contact_backup_or_overall_contact_or_contact_backup_or_contact.save()
            #trial.overall_contact_backup_or_overall_contact_or_contact_backup_or_contacts.add(overall_contact_backup_or_overall_contact_or_contact_backup_or_contact)

        ##
        ## class: responsible_party
        ##

        responsible_partys_hashset = set()

        responsible_party_results = p.findall('responsible_party')
        for responsible_party_result in responsible_party_results:
            responsible_party_hashset = set()
            organization = ''
            organization_result = responsible_party_result.findall('organization')
            if organization_result:
                organization = organization_result[0].text
                responsible_party_hashset.add(organization_result[0].text)
            responsible_party_hashset = set()
            name_title = ''
            name_title_result = responsible_party_result.findall('name_title')
            if name_title_result:
                name_title = name_title_result[0].text
                responsible_party_hashset.add(name_title_result[0].text)
            slug = hashlib.md5(str(responsible_party_hashset)).hexdigest()
            #responsible_party_name = ...
            responsible_party, created = models.Responsible_party.objects.get_or_create(
                            #name = responsible_party_name,
                            name = slug,
                            slug = slug,
                            organization = organization,
                            name_title = name_title,
                            )
            responsible_party.provenances.add(provenance)

            responsible_partys_hashset = responsible_partys_hashset.union(responsible_party_hashset)
            responsible_party.save()
            #trial.responsible_partys.add(responsible_party)

        ##
        ## class: detailed_description
        ##

        detailed_descriptions_hashset = set()

        detailed_description_results = p.findall('detailed_description')
        for detailed_description_result in detailed_description_results:
            detailed_description_hashset = set()
            textblock = ''
            textblock_result = detailed_description_result.findall('textblock')
            if textblock_result:
                textblock = textblock_result[0].text
                detailed_description_hashset.add(textblock_result[0].text)
            slug = hashlib.md5(str(detailed_description_hashset)).hexdigest()
            #detailed_description_name = ...
            detailed_description, created = models.Detailed_description.objects.get_or_create(
                            #name = detailed_description_name,
                            name = slug,
                            slug = slug,
                            textblock = textblock,
                            )
            detailed_description.provenances.add(provenance)

            detailed_descriptions_hashset = detailed_descriptions_hashset.union(detailed_description_hashset)
            detailed_description.save()
            #trial.detailed_descriptions.add(detailed_description)

        ##
        ## class: intervention
        ##

        interventions_hashset = set()

        intervention_results = p.findall('intervention')
        for intervention_result in intervention_results:
            intervention_hashset = set()
            arm_group_label = ''
            arm_group_label_result = intervention_result.findall('arm_group_label')
            if arm_group_label_result:
                arm_group_label = arm_group_label_result[0].text
                intervention_hashset.add(arm_group_label_result[0].text)
            intervention_hashset = set()
            description = ''
            description_result = intervention_result.findall('description')
            if description_result:
                description = description_result[0].text
                intervention_hashset.add(description_result[0].text)
            intervention_hashset = set()
            other_name = ''
            other_name_result = intervention_result.findall('other_name')
            if other_name_result:
                other_name = other_name_result[0].text
                intervention_hashset.add(other_name_result[0].text)
            intervention_hashset = set()
            intervention_type = ''
            intervention_type_result = intervention_result.findall('intervention_type')
            if intervention_type_result:
                intervention_type = intervention_type_result[0].text
                intervention_hashset.add(intervention_type_result[0].text)
            intervention_hashset = set()
            intervention_name = ''
            intervention_name_result = intervention_result.findall('intervention_name')
            if intervention_name_result:
                intervention_name = intervention_name_result[0].text
                intervention_hashset.add(intervention_name_result[0].text)
            slug = hashlib.md5(str(intervention_hashset)).hexdigest()
            #intervention_name = ...
            intervention, created = models.Intervention.objects.get_or_create(
                            #name = intervention_name,
                            name = slug,
                            slug = slug,
                            arm_group_label = arm_group_label,
                            description = description,
                            other_name = other_name,
                            intervention_type = intervention_type,
                            intervention_name = intervention_name,
                            )
            intervention.provenances.add(provenance)

            interventions_hashset = interventions_hashset.union(intervention_hashset)
            intervention.save()
            #trial.interventions.add(intervention)

        ##
        ## class: city
        ##

        citys_hashset = set()

        city_results = p.findall('location/facility/address/city')
        for city_result in city_results:
            city_hashset = set()
            if city_results:
                city_name = city_results[0].text
                city_hashset.add(city_result[0].text)
            slug = hashlib.md5(str(city_hashset)).hexdigest()
            #city_name = ...
            city, created = models.City.objects.get_or_create(
                            #name = city_name,
                            name = slug,
                            slug = slug,
                            city_name = city_name,
                            )
            city.provenances.add(provenance)

            citys_hashset = citys_hashset.union(city_hashset)
            city.save()
            #trial.citys.add(city)

        ##
        ## class: clinical_study
        ##

        clinical_studys_hashset = set()

        ##
        ## class: results_reference_or_reference
        ##

        results_reference_or_references_hashset = set()

        results_reference_or_reference_results = p.findall('results_reference')
        for results_reference_or_reference_result in results_reference_or_reference_results:
            results_reference_or_reference_hashset = set()
            citation = ''
            citation_result = results_reference_or_reference_result.findall('citation')
            if citation_result:
                citation = citation_result[0].text
                results_reference_or_reference_hashset.add(citation_result[0].text)
            results_reference_or_reference_hashset = set()
            PMID = ''
            PMID_result = results_reference_or_reference_result.findall('PMID')
            if PMID_result:
                PMID = PMID_result[0].text
                results_reference_or_reference_hashset.add(PMID_result[0].text)
            slug = hashlib.md5(str(results_reference_or_reference_hashset)).hexdigest()
            #results_reference_or_reference_name = ...
            results_reference_or_reference, created = models.Results_reference_or_reference.objects.get_or_create(
                            #name = results_reference_or_reference_name,
                            name = slug,
                            slug = slug,
                            citation = citation,
                            PMID = PMID,
                            )
            results_reference_or_reference.provenances.add(provenance)

            results_reference_or_references_hashset = results_reference_or_references_hashset.union(results_reference_or_reference_hashset)
            results_reference_or_reference.save()
            #trial.results_reference_or_references.add(results_reference_or_reference)

        results_reference_or_reference_results = p.findall('reference')
        for results_reference_or_reference_result in results_reference_or_reference_results:
            results_reference_or_reference_hashset = set()
            citation = ''
            citation_result = results_reference_or_reference_result.findall('citation')
            if citation_result:
                citation = citation_result[0].text
                results_reference_or_reference_hashset.add(citation_result[0].text)
            results_reference_or_reference_hashset = set()
            PMID = ''
            PMID_result = results_reference_or_reference_result.findall('PMID')
            if PMID_result:
                PMID = PMID_result[0].text
                results_reference_or_reference_hashset.add(PMID_result[0].text)
            slug = hashlib.md5(str(results_reference_or_reference_hashset)).hexdigest()
            #results_reference_or_reference_name = ...
            results_reference_or_reference, created = models.Results_reference_or_reference.objects.get_or_create(
                            #name = results_reference_or_reference_name,
                            name = slug,
                            slug = slug,
                            citation = citation,
                            PMID = PMID,
                            )
            results_reference_or_reference.provenances.add(provenance)

            results_reference_or_references_hashset = results_reference_or_references_hashset.union(results_reference_or_reference_hashset)
            results_reference_or_reference.save()
            #trial.results_reference_or_references.add(results_reference_or_reference)

        ##
        ## class: state
        ##

        states_hashset = set()

        state_results = p.findall('location/facility/address/state')
        for state_result in state_results:
            state_hashset = set()
            if state_results:
                state_name = state_results[0].text
                state_hashset.add(state_result[0].text)
            slug = hashlib.md5(str(state_hashset)).hexdigest()
            #state_name = ...
            state, created = models.State.objects.get_or_create(
                            #name = state_name,
                            name = slug,
                            slug = slug,
                            state_name = state_name,
                            )
            state.provenances.add(provenance)

            states_hashset = states_hashset.union(state_hashset)
            state.save()
            #trial.states.add(state)

        ##
        ## class: location
        ##

        locations_hashset = set()

        location_results = p.findall('location')
        for location_result in location_results:
            location_hashset = set()
            status = ''
            status_result = location_result.findall('status')
            if status_result:
                status = status_result[0].text
                location_hashset.add(status_result[0].text)
            slug = hashlib.md5(str(location_hashset)).hexdigest()
            #location_name = ...
            location, created = models.Location.objects.get_or_create(
                            #name = location_name,
                            name = slug,
                            slug = slug,
                            status = status,
                            )
            location.provenances.add(provenance)

            locations_hashset = locations_hashset.union(location_hashset)
            location.save()
            #trial.locations.add(location)

        ##
        ## class: collaborator_or_lead_sponsor
        ##

        collaborator_or_lead_sponsors_hashset = set()

        collaborator_or_lead_sponsor_results = p.findall('sponsors/collaborator')
        for collaborator_or_lead_sponsor_result in collaborator_or_lead_sponsor_results:
            collaborator_or_lead_sponsor_hashset = set()
            agency_class = ''
            agency_class_result = collaborator_or_lead_sponsor_result.findall('agency_class')
            if agency_class_result:
                agency_class = agency_class_result[0].text
                collaborator_or_lead_sponsor_hashset.add(agency_class_result[0].text)
            collaborator_or_lead_sponsor_hashset = set()
            agency = ''
            agency_result = collaborator_or_lead_sponsor_result.findall('agency')
            if agency_result:
                agency = agency_result[0].text
                collaborator_or_lead_sponsor_hashset.add(agency_result[0].text)
            slug = hashlib.md5(str(collaborator_or_lead_sponsor_hashset)).hexdigest()
            #collaborator_or_lead_sponsor_name = ...
            collaborator_or_lead_sponsor, created = models.Collaborator_or_lead_sponsor.objects.get_or_create(
                            #name = collaborator_or_lead_sponsor_name,
                            name = slug,
                            slug = slug,
                            agency_class = agency_class,
                            agency = agency,
                            )
            collaborator_or_lead_sponsor.provenances.add(provenance)

            collaborator_or_lead_sponsors_hashset = collaborator_or_lead_sponsors_hashset.union(collaborator_or_lead_sponsor_hashset)
            collaborator_or_lead_sponsor.save()
            #trial.collaborator_or_lead_sponsors.add(collaborator_or_lead_sponsor)

        collaborator_or_lead_sponsor_results = p.findall('sponsors/lead_sponsor')
        for collaborator_or_lead_sponsor_result in collaborator_or_lead_sponsor_results:
            collaborator_or_lead_sponsor_hashset = set()
            agency_class = ''
            agency_class_result = collaborator_or_lead_sponsor_result.findall('agency_class')
            if agency_class_result:
                agency_class = agency_class_result[0].text
                collaborator_or_lead_sponsor_hashset.add(agency_class_result[0].text)
            collaborator_or_lead_sponsor_hashset = set()
            agency = ''
            agency_result = collaborator_or_lead_sponsor_result.findall('agency')
            if agency_result:
                agency = agency_result[0].text
                collaborator_or_lead_sponsor_hashset.add(agency_result[0].text)
            slug = hashlib.md5(str(collaborator_or_lead_sponsor_hashset)).hexdigest()
            #collaborator_or_lead_sponsor_name = ...
            collaborator_or_lead_sponsor, created = models.Collaborator_or_lead_sponsor.objects.get_or_create(
                            #name = collaborator_or_lead_sponsor_name,
                            name = slug,
                            slug = slug,
                            agency_class = agency_class,
                            agency = agency,
                            )
            collaborator_or_lead_sponsor.provenances.add(provenance)

            collaborator_or_lead_sponsors_hashset = collaborator_or_lead_sponsors_hashset.union(collaborator_or_lead_sponsor_hashset)
            collaborator_or_lead_sponsor.save()
            #trial.collaborator_or_lead_sponsors.add(collaborator_or_lead_sponsor)

        ##
        ## class: eligibility
        ##

        eligibilitys_hashset = set()

        eligibility_results = p.findall('eligibility')
        for eligibility_result in eligibility_results:
            eligibility_hashset = set()
            criteria_textblock = ''
            criteria_textblock_result = eligibility_result.findall('criteria/textblock')
            if criteria_textblock_result:
                criteria_textblock = criteria_textblock_result[0].text
                eligibility_hashset.add(criteria_textblock_result[0].text)
            eligibility_hashset = set()
            maximum_age = ''
            maximum_age_result = eligibility_result.findall('maximum_age')
            if maximum_age_result:
                maximum_age = maximum_age_result[0].text
                eligibility_hashset.add(maximum_age_result[0].text)
            eligibility_hashset = set()
            healthy_volunteers = ''
            healthy_volunteers_result = eligibility_result.findall('healthy_volunteers')
            if healthy_volunteers_result:
                healthy_volunteers = healthy_volunteers_result[0].text
                eligibility_hashset.add(healthy_volunteers_result[0].text)
            eligibility_hashset = set()
            study_pop_textblock = ''
            study_pop_textblock_result = eligibility_result.findall('study_pop/textblock')
            if study_pop_textblock_result:
                study_pop_textblock = study_pop_textblock_result[0].text
                eligibility_hashset.add(study_pop_textblock_result[0].text)
            eligibility_hashset = set()
            minimum_age = ''
            minimum_age_result = eligibility_result.findall('minimum_age')
            if minimum_age_result:
                minimum_age = minimum_age_result[0].text
                eligibility_hashset.add(minimum_age_result[0].text)
            eligibility_hashset = set()
            gender = ''
            gender_result = eligibility_result.findall('gender')
            if gender_result:
                gender = gender_result[0].text
                eligibility_hashset.add(gender_result[0].text)
            eligibility_hashset = set()
            sampling_method = ''
            sampling_method_result = eligibility_result.findall('sampling_method')
            if sampling_method_result:
                sampling_method = sampling_method_result[0].text
                eligibility_hashset.add(sampling_method_result[0].text)
            slug = hashlib.md5(str(eligibility_hashset)).hexdigest()
            #eligibility_name = ...
            eligibility, created = models.Eligibility.objects.get_or_create(
                            #name = eligibility_name,
                            name = slug,
                            slug = slug,
                            criteria_textblock = criteria_textblock,
                            maximum_age = maximum_age,
                            healthy_volunteers = healthy_volunteers,
                            study_pop_textblock = study_pop_textblock,
                            minimum_age = minimum_age,
                            gender = gender,
                            sampling_method = sampling_method,
                            )
            eligibility.provenances.add(provenance)

            eligibilitys_hashset = eligibilitys_hashset.union(eligibility_hashset)
            eligibility.save()
            #trial.eligibilitys.add(eligibility)

        ##
        ## class: arm_group
        ##

        arm_groups_hashset = set()

        arm_group_results = p.findall('arm_group')
        for arm_group_result in arm_group_results:
            arm_group_hashset = set()
            arm_group_label = ''
            arm_group_label_result = arm_group_result.findall('arm_group_label')
            if arm_group_label_result:
                arm_group_label = arm_group_label_result[0].text
                arm_group_hashset.add(arm_group_label_result[0].text)
            arm_group_hashset = set()
            description = ''
            description_result = arm_group_result.findall('description')
            if description_result:
                description = description_result[0].text
                arm_group_hashset.add(description_result[0].text)
            arm_group_hashset = set()
            arm_group_type = ''
            arm_group_type_result = arm_group_result.findall('arm_group_type')
            if arm_group_type_result:
                arm_group_type = arm_group_type_result[0].text
                arm_group_hashset.add(arm_group_type_result[0].text)
            slug = hashlib.md5(str(arm_group_hashset)).hexdigest()
            #arm_group_name = ...
            arm_group, created = models.Arm_group.objects.get_or_create(
                            #name = arm_group_name,
                            name = slug,
                            slug = slug,
                            arm_group_label = arm_group_label,
                            description = description,
                            arm_group_type = arm_group_type,
                            )
            arm_group.provenances.add(provenance)

            arm_groups_hashset = arm_groups_hashset.union(arm_group_hashset)
            arm_group.save()
            #trial.arm_groups.add(arm_group)

        ##
        ## class: sponsors
        ##

        sponsorss_hashset = set()

        sponsors_results = p.findall('sponsors')
        for sponsors_result in sponsors_results:
            slug = hashlib.md5(str(sponsors_hashset)).hexdigest()
            #sponsors_name = ...
            sponsors, created = models.Sponsors.objects.get_or_create(
                            #name = sponsors_name,
                            name = slug,
                            slug = slug,
                            )
            sponsors.provenances.add(provenance)

            sponsorss_hashset = sponsorss_hashset.union(sponsors_hashset)
            sponsors.save()
            #trial.sponsorss.add(sponsors)

        ##
        ## class: overall_official
        ##

        overall_officials_hashset = set()

        overall_official_results = p.findall('overall_official')
        for overall_official_result in overall_official_results:
            overall_official_hashset = set()
            last_name = ''
            last_name_result = overall_official_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_official_hashset.add(last_name_result[0].text)
            overall_official_hashset = set()
            role = ''
            role_result = overall_official_result.findall('role')
            if role_result:
                role = role_result[0].text
                overall_official_hashset.add(role_result[0].text)
            overall_official_hashset = set()
            affiliation = ''
            affiliation_result = overall_official_result.findall('affiliation')
            if affiliation_result:
                affiliation = affiliation_result[0].text
                overall_official_hashset.add(affiliation_result[0].text)
            slug = hashlib.md5(str(overall_official_hashset)).hexdigest()
            #overall_official_name = ...
            overall_official, created = models.Overall_official.objects.get_or_create(
                            #name = overall_official_name,
                            name = slug,
                            slug = slug,
                            last_name = last_name,
                            role = role,
                            affiliation = affiliation,
                            )
            overall_official.provenances.add(provenance)

            overall_officials_hashset = overall_officials_hashset.union(overall_official_hashset)
            overall_official.save()
            #trial.overall_officials.add(overall_official)

        ##
        ## class: biospec_descr
        ##

        biospec_descrs_hashset = set()

        biospec_descr_results = p.findall('biospec_descr')
        for biospec_descr_result in biospec_descr_results:
            biospec_descr_hashset = set()
            textblock = ''
            textblock_result = biospec_descr_result.findall('textblock')
            if textblock_result:
                textblock = textblock_result[0].text
                biospec_descr_hashset.add(textblock_result[0].text)
            slug = hashlib.md5(str(biospec_descr_hashset)).hexdigest()
            #biospec_descr_name = ...
            biospec_descr, created = models.Biospec_descr.objects.get_or_create(
                            #name = biospec_descr_name,
                            name = slug,
                            slug = slug,
                            textblock = textblock,
                            )
            biospec_descr.provenances.add(provenance)

            biospec_descrs_hashset = biospec_descrs_hashset.union(biospec_descr_hashset)
            biospec_descr.save()
            #trial.biospec_descrs.add(biospec_descr)

        ##
        ## class: address
        ##

        addresss_hashset = set()

        address_results = p.findall('location/facility/address')
        for address_result in address_results:
            address_hashset = set()
            zip = ''
            zip_result = address_result.findall('zip')
            if zip_result:
                zip = zip_result[0].text
                address_hashset.add(zip_result[0].text)
            slug = hashlib.md5(str(address_hashset)).hexdigest()
            #address_name = ...
            address, created = models.Address.objects.get_or_create(
                            #name = address_name,
                            name = slug,
                            slug = slug,
                            zip = zip,
                            )
            address.provenances.add(provenance)

            addresss_hashset = addresss_hashset.union(address_hashset)
            address.save()
            #trial.addresss.add(address)

        ##
        ## class: mesh_term
        ##

        mesh_terms_hashset = set()

        mesh_term_results = p.findall('condition_browse/mesh_term')
        for mesh_term_result in mesh_term_results:
            mesh_term_hashset = set()
            if mesh_term_results:
                mesh_term = mesh_term_results[0].text
                mesh_term_hashset.add(mesh_term_result[0].text)
            slug = hashlib.md5(str(mesh_term_hashset)).hexdigest()
            #mesh_term_name = ...
            mesh_term, created = models.Mesh_term.objects.get_or_create(
                            #name = mesh_term_name,
                            name = slug,
                            slug = slug,
                            mesh_term = mesh_term,
                            )
            mesh_term.provenances.add(provenance)

            mesh_terms_hashset = mesh_terms_hashset.union(mesh_term_hashset)
            mesh_term.save()
            #trial.mesh_terms.add(mesh_term)

        mesh_term_results = p.findall('intervention_browse/mesh_term')
        for mesh_term_result in mesh_term_results:
            mesh_term_hashset = set()
            if mesh_term_results:
                mesh_term = mesh_term_results[0].text
                mesh_term_hashset.add(mesh_term_result[0].text)
            slug = hashlib.md5(str(mesh_term_hashset)).hexdigest()
            #mesh_term_name = ...
            mesh_term, created = models.Mesh_term.objects.get_or_create(
                            #name = mesh_term_name,
                            name = slug,
                            slug = slug,
                            mesh_term = mesh_term,
                            )
            mesh_term.provenances.add(provenance)

            mesh_terms_hashset = mesh_terms_hashset.union(mesh_term_hashset)
            mesh_term.save()
            #trial.mesh_terms.add(mesh_term)

        ##
        ## class: location_countries
        ##

        location_countriess_hashset = set()

        location_countries_results = p.findall('location_countries')
        for location_countries_result in location_countries_results:
            slug = hashlib.md5(str(location_countries_hashset)).hexdigest()
            #location_countries_name = ...
            location_countries, created = models.Location_countries.objects.get_or_create(
                            #name = location_countries_name,
                            name = slug,
                            slug = slug,
                            )
            location_countries.provenances.add(provenance)

            location_countriess_hashset = location_countriess_hashset.union(location_countries_hashset)
            location_countries.save()
            #trial.location_countriess.add(location_countries)

        ##
        ## class: investigator
        ##

        investigators_hashset = set()

        investigator_results = p.findall('location/investigator')
        for investigator_result in investigator_results:
            investigator_hashset = set()
            last_name = ''
            last_name_result = investigator_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                investigator_hashset.add(last_name_result[0].text)
            investigator_hashset = set()
            role = ''
            role_result = investigator_result.findall('role')
            if role_result:
                role = role_result[0].text
                investigator_hashset.add(role_result[0].text)
            slug = hashlib.md5(str(investigator_hashset)).hexdigest()
            #investigator_name = ...
            investigator, created = models.Investigator.objects.get_or_create(
                            #name = investigator_name,
                            name = slug,
                            slug = slug,
                            last_name = last_name,
                            role = role,
                            )
            investigator.provenances.add(provenance)

            investigators_hashset = investigators_hashset.union(investigator_hashset)
            investigator.save()
            #trial.investigators.add(investigator)

        ##
        ## class: country
        ##

        countrys_hashset = set()

        country_results = p.findall('location/facility/address/country')
        for country_result in country_results:
            country_hashset = set()
            if country_results:
                country_name = country_results[0].text
                country_hashset.add(country_result[0].text)
            slug = hashlib.md5(str(country_hashset)).hexdigest()
            #country_name = ...
            country, created = models.Country.objects.get_or_create(
                            #name = country_name,
                            name = slug,
                            slug = slug,
                            country_name = country_name,
                            )
            country.provenances.add(provenance)

            countrys_hashset = countrys_hashset.union(country_hashset)
            country.save()
            #trial.countrys.add(country)

        ##
        ## class: oversight_info
        ##

        oversight_infos_hashset = set()

        oversight_info_results = p.findall('oversight_info')
        for oversight_info_result in oversight_info_results:
            oversight_info_hashset = set()
            authority = ''
            authority_result = oversight_info_result.findall('authority')
            if authority_result:
                authority = authority_result[0].text
                oversight_info_hashset.add(authority_result[0].text)
            oversight_info_hashset = set()
            has_dmc = ''
            has_dmc_result = oversight_info_result.findall('has_dmc')
            if has_dmc_result:
                has_dmc = has_dmc_result[0].text
                oversight_info_hashset.add(has_dmc_result[0].text)
            slug = hashlib.md5(str(oversight_info_hashset)).hexdigest()
            #oversight_info_name = ...
            oversight_info, created = models.Oversight_info.objects.get_or_create(
                            #name = oversight_info_name,
                            name = slug,
                            slug = slug,
                            authority = authority,
                            has_dmc = has_dmc,
                            )
            oversight_info.provenances.add(provenance)

            oversight_infos_hashset = oversight_infos_hashset.union(oversight_info_hashset)
            oversight_info.save()
            #trial.oversight_infos.add(oversight_info)

        ##
        ## class: intervention_browse
        ##

        intervention_browses_hashset = set()

        intervention_browse_results = p.findall('intervention_browse')
        for intervention_browse_result in intervention_browse_results:
            intervention_browse_hashset = set()
            mesh_term = ''
            mesh_term_result = intervention_browse_result.findall('mesh_term')
            if mesh_term_result:
                mesh_term = mesh_term_result[0].text
                intervention_browse_hashset.add(mesh_term_result[0].text)
            slug = hashlib.md5(str(intervention_browse_hashset)).hexdigest()
            #intervention_browse_name = ...
            intervention_browse, created = models.Intervention_browse.objects.get_or_create(
                            #name = intervention_browse_name,
                            name = slug,
                            slug = slug,
                            mesh_term = mesh_term,
                            )
            intervention_browse.provenances.add(provenance)

            intervention_browses_hashset = intervention_browses_hashset.union(intervention_browse_hashset)
            intervention_browse.save()
            #trial.intervention_browses.add(intervention_browse)

        ##
        ## class: link
        ##

        links_hashset = set()

        link_results = p.findall('link')
        for link_result in link_results:
            link_hashset = set()
            description = ''
            description_result = link_result.findall('description')
            if description_result:
                description = description_result[0].text
                link_hashset.add(description_result[0].text)
            link_hashset = set()
            url = ''
            url_result = link_result.findall('url')
            if url_result:
                url = url_result[0].text
                link_hashset.add(url_result[0].text)
            slug = hashlib.md5(str(link_hashset)).hexdigest()
            #link_name = ...
            link, created = models.Link.objects.get_or_create(
                            #name = link_name,
                            name = slug,
                            slug = slug,
                            description = description,
                            url = url,
                            )
            link.provenances.add(provenance)

            links_hashset = links_hashset.union(link_hashset)
            link.save()
            #trial.links.add(link)

        ##
        ## class: condition_browse
        ##

        condition_browses_hashset = set()

        condition_browse_results = p.findall('condition_browse')
        for condition_browse_result in condition_browse_results:
            slug = hashlib.md5(str(condition_browse_hashset)).hexdigest()
            #condition_browse_name = ...
            condition_browse, created = models.Condition_browse.objects.get_or_create(
                            #name = condition_browse_name,
                            name = slug,
                            slug = slug,
                            )
            condition_browse.provenances.add(provenance)

            condition_browses_hashset = condition_browses_hashset.union(condition_browse_hashset)
            condition_browse.save()
            #trial.condition_browses.add(condition_browse)
