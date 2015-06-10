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

import hashlib
import urllib2
import chardet
import models
from xml.etree.ElementTree import fromstring 
#from elementtree.ElementTree import fromstring
from xml.parsers.expat import ExpatError

from django.template.defaultfilters import slugify
from geopy import geocoders

class UrlException(urllib2.URLError):
    """Exception for URL read error.

    Simply inherit from URLError. The reason not to use URLError directly is
    for better encapsulation.
    """
    pass


class FileSizeLimitExceededException(Exception):
    """Exception for file size exceeding limit."""
    def __init__(self, limit):
        self.limit = limit

    def __str__(self):
        return "File size exceeds limit %d KB." % (self.limit / 1024)


class XMLFileFormatException(Exception):
    """Exception for an invalid xml formatted file."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def process_xml(url, size_limit, client_ip, encoding=None, reprocess=False):
    """Process an incoming XML file."""

    if url.startswith("http://clinicaltrials.gov/show/"):
        if (len(url)<42):
            raise XMLFileFormatException("Bad URL: " + url)
        url = "http://clinicaltrials.gov/show/" + url[31:42] + "?displayxml=true"
    else:
        raise XMLFileFormatException("Bad URL: " + url)

    # Download the file.
    content = download_url(url, size_limit)
    #content = xml_utils.preprocess_xml(content)

    # Calculate the hash signature. This must be done before any conversion.
    signature = hashlib.md5(content).hexdigest()

    # See if provenance exists.
    provenance, created = models.Provenance.objects.get_or_create(url=url)
    
    old_signature = provenance.signature

    # Only reload the file if the hash signature is different.
    
    #
    # TODO: fix this when done debuggin!
    #
    #if old_signature != signature:
    if reprocess or (old_signature != signature):
        # Removing everything from associated with the old provenance
        for (o, m) in provenance._meta.get_all_related_m2m_objects_with_model():
            objectlist = provenance.__getattribute__(o.var_name + '_set').all()
            for object in objectlist:
                object.provenances.remove(provenance)
                if len(object.provenances.all())==0:
                    links = models.External_linkage.objects.filter(from_object_slug=object.slug)
                    for link in links:
                        link.delete()
                    links = models.Linkage.objects.filter(from_object_slug=object.slug)
                    for link in links:
                        link.delete()
                    object.delete()
                    #print str(object) + ' deleted'
        provenance.delete()
        provenance = models.Provenance.objects.create(url=url)
        
        provenance.ip = client_ip
        provenance.time_added = provenance.time_added

        # Detect encoding.
        if encoding is None or not encoding:
            chardet_encoding = chardet.detect(content)
            encoding = chardet_encoding['encoding']
            if not encoding:
                encoding = 'utf-8'

        provenance.encoding = encoding

        # Convert to unicode.
        content = content.decode(encoding)

        
        try:
            p = fromstring(content.encode('utf-8'))
        except ExpatError, e:
            raise XMLFileFormatException(str(e))
            
        result = p.findall('id_info/nct_id')
        if result:
            trialid = result[0].text
        else:
            raise XMLFileFormatException("Trial ID not found in URL: " + url)
        
        id_info_nct_id = trialid
        lookup_name = trialid
        label = trialid
    
        biospec_descr = ''
        result = p.findall('biospec_descr/textblock')
        if result:
            biospec_descr = result[0].text
            
        detailed_description = ''
        result = p.findall('detailed_description/textblock')
        if result:
            detailed_description = result[0].text
    
        lastchanged_date = ''
        result = p.findall('lastchanged_date')
        if result:
            lastchanged_date = result[0].text

        firstreceived_results_date = ''
        result = p.findall('firstreceived_results_date')
        if result:
            firstreceived_results_date = result[0].text

        firstreceived_date = ''
        result = p.findall('firstreceived_date')
        if result:
            firstreceived_date = result[0].text

        overall_status = ''
        result = p.findall('overall_status')
        if result:
            overall_status = result[0].text

        id_info_secondary_id = ''
        result = p.findall('id_info/secondary_id')
        if result:
            id_info_secondary_id = result[0].text

        biospec_retention = ''
        result = p.findall('biospec/retention')
        if result:
            biospec_retention = result[0].text

        required_header_link_text = ''
        result = p.findall('required_header/link_text')
        if result:
            required_header_link_text = result[0].text

        enrollment = ''
        result = p.findall('enrollment')
        if result:
            enrollment = result[0].text

        number_of_arms = ''
        result = p.findall('number_of_arms')
        if result:
            number_of_arms = result[0].text

        is_section_801 = ''
        result = p.findall('is_section_801')
        if result:
            is_section_801 = result[0].text

        is_fda_regulated = ''
        result = p.findall('is_fda_regulated')
        if result:
            is_fda_regulated = result[0].text

        brief_title = ''
        result = p.findall('brief_title')
        if result:
            brief_title = result[0].text

        acronym = ''
        result = p.findall('acronym')
        if result:
            acronym = result[0].text

        official_title = ''
        result = p.findall('official_title')
        if result:
            official_title = result[0].text

        study_type = ''
        result = p.findall('study_type')
        if result:
            study_type = result[0].text

        id_info_nct_alias = ''
        result = p.findall('id_info/nct_alias')
        if result:
            id_info_nct_alias = result[0].text

        completion_date = ''
        result = p.findall('completion_date')
        if result:
            completion_date = result[0].text

        verification_date = ''
        result = p.findall('verification_date')
        if result:
            verification_date = result[0].text

        why_stopped = ''
        result = p.findall('why_stopped')
        if result:
            why_stopped = result[0].text

        id_info_org_study_id = ''
        result = p.findall('id_info/org_study_id')
        if result:
            id_info_org_study_id = result[0].text

        required_header_url = ''
        result = p.findall('required_header/url')
        if result:
            required_header_url = result[0].text

        study_design = ''
        result = p.findall('study_design')
        if result:
            study_design = result[0].text

        source = ''
        result = p.findall('source')
        if result:
            source = result[0].text

        primary_completion_date = ''
        result = p.findall('primary_completion_date')
        if result:
            primary_completion_date = result[0].text

        brief_summary_textblock = ''
        result = p.findall('brief_summary_textblock')
        if result:
            brief_summary_textblock = result[0].text

        number_of_groups = ''
        result = p.findall('number_of_groups')
        if result:
            number_of_groups = result[0].text

        required_header_download_date = ''
        result = p.findall('required_header/download_date')
        if result:
            required_header_download_date = result[0].text

        phase = ''
        result = p.findall('phase')
        if result:
            phase = result[0].text

        start_date = ''
        result = p.findall('start_date')
        if result:
            start_date = result[0].text

        has_expanded_access = ''
        result = p.findall('has_expanded_access')
        if result:
            has_expanded_access = result[0].text
        
        try:
            trial = models.Trial.objects.create(
                        provenance = provenance,
                        label = label,
                        trialid = trialid,
                        lookup_name = lookup_name,
                        lastchanged_date = lastchanged_date,
                        firstreceived_results_date = firstreceived_results_date,
                        firstreceived_date = firstreceived_date,
                        id_info_nct_id = id_info_nct_id,
                        overall_status = overall_status,
                        id_info_secondary_id = id_info_secondary_id,
                        biospec_retention = biospec_retention,
                        required_header_link_text = required_header_link_text,
                        enrollment = enrollment,
                        number_of_arms = number_of_arms,
                        is_section_801 = is_section_801,
                        is_fda_regulated = is_fda_regulated,
                        brief_title = brief_title,
                        acronym = acronym,
                        official_title = official_title,
                        study_type = study_type,
                        id_info_nct_alias = id_info_nct_alias,
                        completion_date = completion_date,
                        verification_date = verification_date,
                        why_stopped = why_stopped,
                        id_info_org_study_id = id_info_org_study_id,
                        required_header_url = required_header_url,
                        study_design = study_design,
                        source = source,
                        primary_completion_date = primary_completion_date,
                        brief_summary = brief_summary_textblock,
                        number_of_groups = number_of_groups,
                        required_header_download_date = required_header_download_date,
                        phase = phase,
                        start_date = start_date,
                        has_expanded_access = has_expanded_access,
                        biospec_descr = biospec_descr,
                        detailed_description = detailed_description,
                        )
        except:
            existing_trial = models.Trial.objects.filter(trialid = trialid)
            if existing_trial:
                existing_trial.delete()
                trial = models.Trial.objects.create(
                        provenance = provenance,
                        label = label,
                        trialid = trialid,
                        lookup_name = lookup_name,
                        lastchanged_date = lastchanged_date,
                        firstreceived_results_date = firstreceived_results_date,
                        firstreceived_date = firstreceived_date,
                        id_info_nct_id = id_info_nct_id,
                        overall_status = overall_status,
                        id_info_secondary_id = id_info_secondary_id,
                        biospec_retention = biospec_retention,
                        required_header_link_text = required_header_link_text,
                        enrollment = enrollment,
                        number_of_arms = number_of_arms,
                        is_section_801 = is_section_801,
                        is_fda_regulated = is_fda_regulated,
                        brief_title = brief_title,
                        acronym = acronym,
                        official_title = official_title,
                        study_type = study_type,
                        id_info_nct_alias = id_info_nct_alias,
                        completion_date = completion_date,
                        verification_date = verification_date,
                        why_stopped = why_stopped,
                        id_info_org_study_id = id_info_org_study_id,
                        required_header_url = required_header_url,
                        study_design = study_design,
                        source = source,
                        primary_completion_date = primary_completion_date,
                        brief_summary = brief_summary_textblock,
                        number_of_groups = number_of_groups,
                        required_header_download_date = required_header_download_date,
                        phase = phase,
                        start_date = start_date,
                        has_expanded_access = has_expanded_access,
                        biospec_descr = biospec_descr,
                        detailed_description = detailed_description,
                        )
        trial.save()

        #
        # 1) location
        # Creating locations entities for the trial
        #

        location_results = p.findall('location')
        for result in location_results:
            location_hasharray = ['Location']
            #
            # The key of location is considered to be concat (city,state,country,zipcode)
            #  or just facility ??? 
            #
            status = ''
            status_result = result.findall('status')
            if status_result:
                status = status_result[0].text
                location_hasharray.append(status + '(status)')

                
            
            # locations has status and 1) facility 2) investigator 3) contact_backup 4) contact
            
            #
            # facility (1-1)
            #
            
            facility = None
            facility_hasharray = ['Facility']

            facility_result = result.findall('facility')
            if facility_result:
                facility_result = facility_result[0]
                facility_name = ''
                name_result = facility_result.findall('name')
                if name_result:
                    facility_name = name_result[0].text
                    facility_hasharray.append(facility_name)
                    
                
                # facility has label and 1) address
                
                #
                # address (1-1)
                #
                
                address = None
                address_hasharray = ['Address']

                address_result = facility_result.findall('address')
                if address_result:
                    address_result = address_result[0]
                    zip = ''
                    zip_result = address_result.findall('zip')
                    if zip_result:
                        zip = zip_result[0].text
                        address_hasharray.append(zip + '(zip)')
                        
                    # address has zip and 1)city 2))state 3)country
                    
                    ##
                    ## class: city
                    ##
            
                    city_result = address_result.findall('city')
                    if city_result:
                        city_name = city_result[0].text
                        if slugify(city_name)=='':
                            city_name = 'N/A'
                        address_hasharray.append(city_name + '(city)')
                        try:
                            city, created = models.City.objects.get_or_create(
                                    label = city_name,
                                    city_name = city_name,
                                    )
                        except:
                            city = models.City.objects.get(
                                    slug = slugify(city_name),
                                    )
                        city.provenances.add(provenance)
                        city.save()
                    else:
                        city_name = ''
                        city = None
                        
                    ##
                    ## class: state
                    ##
            
                    state_result = address_result.findall('state')
                    if state_result:
                        state_name = state_result[0].text
                        if slugify(state_name )=='':
                            state_name  = 'N/A'
                        address_hasharray.append(state_name + '(state)')
                        try:
                            state, created = models.State.objects.get_or_create(
                                    label = state_name,
                                    state_name = state_name,
                                    )
                        except:
                            state, created = models.State.objects.get_or_create(
                                    slug = slugify(state_name),
                                    )
                        state.provenances.add(provenance)
                        state.save()
                    else:
                        state_name = ''
                        state = None
                        
                    ##
                    ## class: country
                    ##
            
                    country_result = address_result.findall('country')
                    if country_result:
                        country_name = country_result[0].text
                        if slugify(country_name)=='':
                            country_name = 'N/A'
                        address_hasharray.append(country_name + '(country)')
                        try:
                            country, created = models.Country.objects.get_or_create(
                                    label = country_name,
                                    country_name = country_name,
                                    )
                        except:
                            country = models.Country.objects.get(
                                    label = country_name,
                                    country_name = country_name,
                                    )
                        country.provenances.add(provenance)
                        country.save()
                    else:
                        country_name = ''
                        country = None
                     
                    address_slug = hashlib.md5(str(address_hasharray)).hexdigest()
                    facility_hasharray.append(address_slug) 
                    address_name = ''
                    if city_name!='':
                        address_name += city_name + ', '
                    if state_name!='':
                        address_name += state_name + ', '
                    if zip!='':
                        address_name += zip + ', '
                    if country_name!='':
                        address_name += country_name + ', '
                    if len(address_name)>2:
                        address_name = address_name[:-2]
                    address_slug = slugify(address_name)
                    if len(models.Address.objects.filter(slug=address_slug)) == 0:
                        address, created = models.Address.objects.get_or_create(
                            label = address_name,
                            slug = address_slug,
                            city = city,
                            state = state,
                            country = country,
                            zip = zip,
                            )
                    else:
                        address = models.Address.objects.get(slug = address_slug)
                    address.provenances.add(provenance)
                    address.save()
                
                if not models.Coordinates.objects.filter(address=address):
                    g = geocoders.Google()
                    add = ""
                    if ("Investigative " in str(address.city)) or ("Various" in str(address.city)) or \
                       ("Multiple" in str(address.city)) or ("To Be Determined" in str(address.city)) or \
                       ("Unknown" in str(address.city)) or ("Cities in " in str(address.city)) or\
                       ("Several" in str(address.city)):
                        if str(address.country) == "Korea, Republic of":
                            add = "South Korea"
                        else:
                            add = address.country
                    elif str(address.country) == "Korea, Republic of":
                        add = str(address.city)+","+str(address.state)+","+str(address.zip)+","\
                              +"South Korea"
                        
                    if not add:
                        add = address
                    
                    results = []
                    try:
                        results = g.geocode(add, exactly_one = False)  
                        
                    except:
                        pass
                    
                    if results:       
                        _, (lat, lng) = results[0]
                        coordinates, created = models.Coordinates.objects.get_or_create(
                            latitude = str(lat),
                            longitude = str(lng),
                            address = address)
                
                else:
                    coordinates = models.Coordinates.objects.get(address=address)
                
                
                        
                facility_slug = hashlib.md5(str(str(facility_hasharray))).hexdigest()
                location_hasharray.append(facility_slug)
                facility_label = facility_slug
                if facility_name!='':
                    facility_label = facility_name
                facility, created = models.Facility.objects.get_or_create(
                                label = facility_label,
                                slug = facility_slug,
                                facility_name = facility_name,
                                address = address,
                                )
                facility.provenances.add(provenance)
                facility.save()
            
            ##
            ## class: investigator
            ##
    
            investigators_hasharray = ['Investigators']
            investigators_list = []
    
            investigator_results = result.findall('investigator')
            for investigator_result in investigator_results:
                investigator_hasharray = ['An Investigator']
                last_name = ''
                last_name_result = investigator_result.findall('last_name')
                if last_name_result:
                    last_name = last_name_result[0].text
                    investigator_hasharray.append(last_name + '(last_name)')
                role = ''
                role_result = investigator_result.findall('role')
                if role_result:
                    role = role_result[0].text
                    investigator_hasharray.append(role + '(role)')
                
                investigator_name = last_name
                if role:
                    investigator_name += ' (' + role + ')'
                
                investigator_slug = hashlib.md5(str(set(investigator_hasharray))).hexdigest()

                investigator, created = models.Investigator.objects.get_or_create(
                                label = investigator_name,
                                slug = investigator_slug,
                                last_name = last_name,
                                role = role,
                                )
                investigator.provenances.add(provenance)
                investigator.save()
                
                investigators_list.append(investigator)
                investigators_hasharray.append(investigator_slug)
            
            investigators_slug = hashlib.md5(str(set(investigators_hasharray))).hexdigest()
            location_hasharray.append(investigators_slug)
            
            ##
            ## class: contact_backup
            ##
    
            contacts_hasharray = ['Contacts']
            contact_backups_list = []
    
            contact_results = result.findall('contact_backup')
            for contact_result in contact_results:
                contact_hasharray = ['A Contact']
                phone_ext = ''
                phone_ext_result = contact_result.findall('phone_ext')
                if phone_ext_result:
                    phone_ext = phone_ext_result[0].text
                    contact_hasharray.append(phone_ext + '(phone_ext)')
                phone = ''
                phone_result = contact_result.findall('phone')
                if phone_result:
                    phone = phone_result[0].text
                    contact_hasharray.append(phone + '(phone)')
                email = ''
                email_result = contact_result.findall('email')
                if email_result:
                    email = email_result[0].text
                    contact_hasharray.append(email + '(email)')
                last_name = ''
                last_name_result = contact_result.findall('last_name')
                if last_name_result:
                    last_name = last_name_result[0].text
                    contact_hasharray.append(last_name+ '(last_name)')
                contactslug = hashlib.md5(str(set(contact_hasharray))).hexdigest()

                contact_name = contactslug
                if last_name:
                    contact_name = last_name + ' (Contact)'
                    
                contact, created = models.Contact.objects.get_or_create(
                                label = contact_name,
                                #label = slug,
                                slug = contactslug,
                                phone_ext = phone_ext,
                                phone = phone,
                                email = email,
                                last_name = last_name,
                                )
                contact.provenances.add(provenance)
                contact.save()
                contact_backups_list.append(contact)
                
            #
            # contact
            #
            
            contacts_list = []
            
            
            contact_results = result.findall('contact')
            for contact_result in contact_results:
                contact_hasharray = ['A Contact']
                phone_ext = ''
                phone_ext_result = contact_result.findall('phone_ext')
                if phone_ext_result:
                    phone_ext = phone_ext_result[0].text
                    contact_hasharray.append(phone_ext + '(phone_ext)')
                phone = ''
                phone_result = contact_result.findall('phone')
                if phone_result:
                    phone = phone_result[0].text
                    contact_hasharray.append(phone + '(phone)')
                email = ''
                email_result = contact_result.findall('email')
                if email_result:
                    email = email_result[0].text
                    contact_hasharray.append(email + '(email)')
                last_name = ''
                last_name_result = contact_result.findall('last_name')
                if last_name_result:
                    last_name = last_name_result[0].text
                    contact_hasharray.append(last_name+ '(last_name)')
                contact_slug = hashlib.md5(str(contact_hasharray)).hexdigest()

                contact_name = contact_slug
                if last_name:
                    contact_name = last_name + ' (Contact)'
                
                contact, created = models.Contact.objects.get_or_create(
                                label = contact_name,
                                #label = slug,
                                slug = contact_slug,
                                phone_ext = phone_ext,
                                phone = phone,
                                email = email,
                                last_name = last_name,
                                )
                contact.provenances.add(provenance)
                contact.save()
                contacts_list.append(contact)
                contacts_hasharray.append(contact_slug)
                
            contacts_slug = hashlib.md5(str(set(contacts_hasharray))).hexdigest()
            location_hasharray.append(contacts_slug)
            
            location_slug = hashlib.md5(str(set(location_hasharray))).hexdigest()
            
            location, created = models.Location.objects.get_or_create(
                            label = location_slug,
                            slug = location_slug,
                            status = status,
                            facility = facility,
                            )
            
            location.provenances.add(provenance)
            
            #if not created:
            #    print "Warning, model not created - it already exists"
            #else:
            #    print created
            #    print "New object created"
            
            for i in investigators_list:
                location.investigators.add(i)
            for i in contact_backups_list:
                location.contact_backups.add(i)
            for i in contacts_list:
                location.contacts.add(i)

            location.save()
            trial.locations.add(location)
            trial.coordinates.add(coordinates)
            
        #
        # 2) condition_browse (1-1)
        #
        
        condition_browse_hasharray = ['Condition Browse']

        condition_browse_results = p.findall('condition_browse')
        if condition_browse_results:
            condition_browse_result = condition_browse_results[0]
            mesh_term_list = []
            mesh_term_results = condition_browse_result.findall('mesh_term')
            for mesh_term_result in mesh_term_results:
                label = mesh_term_result.text
                condition_browse_hasharray.append(label)
                mesh_term_slug = slugify(label)
                if len(mesh_term_slug)>127:
                    slug = hashlib.md5(mesh_term_slug).hexdigest()
                try:
                    mesh_term, created = models.Mesh_term.objects.get_or_create(
                                label = label,
                                slug = mesh_term_slug,
                                )
                except:
                    mesh_term = models.Mesh_term.objects.get(
                                slug = mesh_term_slug,
                                )
                mesh_term.provenances.add(provenance)
                mesh_term.save()
                mesh_term_list.append(mesh_term)
            
            condition_browse_slug = hashlib.md5(str(set(condition_browse_hasharray))).hexdigest()
            
            condition_browse, created = models.Condition_browse.objects.get_or_create(
                        label = condition_browse_slug,
                        )
            condition_browse.provenances.add(provenance)
            
            for mesh_term in mesh_term_list:
                condition_browse.mesh_terms.add(mesh_term)
                
            condition_browse.save()
            
            trial.condition_browse = condition_browse

        #
        # 3) intervention_browse
        #
        
        intervention_browse_hasharray = ['Intervention Browse']

        intervention_browse_results = p.findall('intervention_browse')
        if intervention_browse_results:
            intervention_browse_result = intervention_browse_results[0]
            mesh_term_list = []
            mesh_term_results = intervention_browse_result.findall('mesh_term')
            for mesh_term_result in mesh_term_results:
                label = mesh_term_result.text
                intervention_browse_hasharray.append(label)
                mesh_term_slug = slugify(label)
                if len(mesh_term_slug)>127:
                    mesh_term_slug = hashlib.md5(mesh_term_slug).hexdigest()
                try:
                    mesh_term, created = models.Mesh_term.objects.get_or_create(
                                label = label,
                                slug = mesh_term_slug,
                                )
                except:
                    mesh_term = models.Mesh_term.objects.get(
                                slug = mesh_term_slug,
                                )
                mesh_term.provenances.add(provenance)
                mesh_term.save()
                mesh_term_list.append(mesh_term)
            
            intervention_browse_slug = hashlib.md5(str(set(intervention_browse_hasharray))).hexdigest()
            
            intervention_browse, created = models.Intervention_browse.objects.get_or_create(
                        label = intervention_browse_slug,
                        )
            intervention_browse.provenances.add(provenance)
            
            for mesh_term in mesh_term_list:
                intervention_browse.mesh_terms.add(mesh_term)
                
            intervention_browse.save()
            
            trial.intervention_browse = intervention_browse
        
        #
        # 4) link
        #
        
        link_results = p.findall('link')
        for link_result in link_results:
            link_hasharray = ['Link']
            description = ''
            description_result = link_result.findall('description')
            if description_result:
                description = description_result[0].text
                link_hasharray.append(description_result[0].text + '(description)')
            url = ''
            url_result = link_result.findall('url')
            if url_result:
                url = url_result[0].text
                link_hasharray.append(url_result[0].text + '(url)')
            link_slug = hashlib.md5(str(set(link_hasharray))).hexdigest()
            link_name = url
            link, created = models.Link.objects.get_or_create(
                            label = link_name,
                            slug = link_slug,
                            description = description,
                            url = url,
                            )
            link.provenances.add(provenance)
            link.save()
            trial.links.add(link)
        
        #
        # 5) responsible_party
        #
        
        responsible_party_results = p.findall('responsible_party')
        if responsible_party_results:
            responsible_party_result = responsible_party_results[0]
            responsible_party_hasharray = ['Responsible Party']
            organization = ''
            organization_result = responsible_party_result.findall('organization')
            if organization_result:
                organization = organization_result[0].text
                responsible_party_hasharray.append(organization_result[0].text)
            name_title = ''
            name_title_result = responsible_party_result.findall('name_title')
            if name_title_result:
                name_title = name_title_result[0].text
                responsible_party_hasharray.append(name_title_result[0].text  + '(name_title)')
            responsible_party_slug = hashlib.md5(str(set(responsible_party_hasharray))).hexdigest()
            
            #responsible_party_name = ...
            responsible_party, created = models.Responsible_party.objects.get_or_create(
                            #label = responsible_party_name,
                            label = responsible_party_slug,
                            slug = responsible_party_slug,
                            organization = organization,
                            name_title = name_title,
                            )

            responsible_party.provenances.add(provenance)
            
            responsible_party.save()
            
            trial.responsible_party = responsible_party
        
        #
        # 6) results_reference
        #
        
        results_reference = p.findall('results_reference')
        for results_reference in results_reference:
            results_reference_hasharray = ['Reference']
            citation = ''
            citation_result = results_reference.findall('citation')
            if citation_result:
                citation = citation_result[0].text
                results_reference_hasharray.append(citation_result[0].text + '(citation)')
            PMID = ''
            PMID_result = results_reference.findall('PMID')
            if PMID_result:
                PMID = PMID_result[0].text
                results_reference_hasharray.append(PMID_result[0].text + '(PMID)')
            results_reference_slug = hashlib.md5(str(set(results_reference_hasharray))).hexdigest()
            results_reference_name = results_reference_slug
            if PMID:
                results_reference_name = 'PMID:' + PMID
            results_reference, created = models.Reference.objects.get_or_create(
                            label = results_reference_name,
                            #slug = slug,
                            citation = citation,
                            PMID = PMID,
                            )
            results_reference.provenances.add(provenance)

            results_reference.save()
            trial.results_references.add(results_reference)
        
        #
        # 7) overall_contact
        #
        
        overall_contact_results = p.findall('overall_contact')
        if overall_contact_results:
            overall_contact_result = overall_contact_results[0]
            overall_contact_hasharray = ['Contact']
            phone_ext = ''
            phone_ext_result = overall_contact_result.findall('phone_ext')
            if phone_ext_result:
                phone_ext = phone_ext_result[0].text
                overall_contact_hasharray.append(phone_ext_result[0].text + '(phone_ext)')
            
            phone = ''
            phone_result = overall_contact_result.findall('phone')
            if phone_result:
                phone = phone_result[0].text
                overall_contact_hasharray.append(phone_result[0].text + '(phone)')
            
            email = ''
            email_result = overall_contact_result.findall('email')
            if email_result:
                email = email_result[0].text
                overall_contact_hasharray.append(email_result[0].text + '(email)')
            
            last_name = ''
            last_name_result = overall_contact_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_contact_hasharray.append(last_name_result[0].text + '(last_name)')
            overall_contact_slug = hashlib.md5(str(set(overall_contact_hasharray))).hexdigest()
            overall_contact_name = overall_contact_slug
            if last_name:
                    overall_contact_name = last_name + ' (Contact)'
            overall_contact, created = models.Contact.objects.get_or_create(
                            label = overall_contact_name,
                            slug = overall_contact_slug,
                            phone_ext = phone_ext,
                            phone = phone,
                            email = email,
                            last_name = last_name,
                            )
            overall_contact.provenances.add(provenance)

            overall_contact.save()
            trial.overall_contact = overall_contact
        
        #
        # 8) arm_group
        #
        
        arm_group_results = p.findall('arm_group')
        for arm_group_result in arm_group_results:
            arm_group_hasharray = ['Arm Group']
            arm_group_label = ''
            arm_group_label_result = arm_group_result.findall('arm_group_label')
            if arm_group_label_result:
                arm_group_label = arm_group_label_result[0].text
                arm_group_hasharray.append(arm_group_label_result[0].text + '(arm_group_label)')
            description = ''
            description_result = arm_group_result.findall('description')
            if description_result:
                description = description_result[0].text
                arm_group_hasharray.append(description_result[0].text + '(description)')
            arm_group_type = ''
            arm_group_type_result = arm_group_result.findall('arm_group_type')
            if arm_group_type_result:
                arm_group_type = arm_group_type_result[0].text
                arm_group_hasharray.append(arm_group_type_result[0].text + '(arm_group_type)')
            arm_group_slug = hashlib.md5(str(set(arm_group_hasharray))).hexdigest()
            arm_group_name = arm_group_slug
            if arm_group_label:
                arm_group_name = arm_group_label + ' (Arm Group)'
            arm_group, created = models.Arm_group.objects.get_or_create(
                            label = arm_group_name,
                            slug = arm_group_slug,
                            arm_group_label = arm_group_label,
                            description = description,
                            arm_group_type = arm_group_type,
                            )
            arm_group.provenances.add(provenance)
            arm_group.save()
            trial.arm_groups.add(arm_group)
        
        #
        # 9) location_countries
        #
        
        location_countries_results = p.findall('location_countries')
        for location_countries_result in location_countries_results:
            country_results = location_countries_result.findall('country')
            for country_result in country_results:
                country_name = country_result.text
                if slugify(country_name)=='':
                        country_name = 'N/A'
                country, created = models.Country.objects.get_or_create(
                                label = country_name,
                                country_name = country_name,
                                )
                country.provenances.add(provenance)
                country.save()
                trial.location_countries.add(country)
        
        #
        # 10) intervention
        #
        
        intervention_results = p.findall('intervention')
        for intervention_result in intervention_results:
            intervention_hasharray = ['Intervention']
            arm_group_label = ''
            arm_group_label_result = intervention_result.findall('arm_group_label')
            if arm_group_label_result:
                arm_group_label = arm_group_label_result[0].text
                intervention_hasharray.append(arm_group_label_result[0].text + '(arm_group_label)')
            description = ''
            description_result = intervention_result.findall('description')
            if description_result:
                description = description_result[0].text
                intervention_hasharray.append(description_result[0].text + '(description)')
            other_name = ''
            other_name_result = intervention_result.findall('other_name')
            if other_name_result:
                other_name = other_name_result[0].text
                intervention_hasharray.append(other_name_result[0].text + '(other_name)')
            intervention_type = ''
            intervention_type_result = intervention_result.findall('intervention_type')
            if intervention_type_result:
                intervention_type = intervention_type_result[0].text
                intervention_hasharray.append(intervention_type_result[0].text + '(intervention_type)')
            intervention_name = ''
            intervention_name_result = intervention_result.findall('intervention_name')
            if intervention_name_result:
                intervention_name = intervention_name_result[0].text
                intervention_hasharray.append(intervention_name_result[0].text + '(intervention_name)')
            intervention_slug = hashlib.md5(str(set(intervention_hasharray))).hexdigest()
            intervention_label = intervention_slug
            if intervention_name:
                intervention_label = intervention_name + ' (Intervention)'
            intervention, created = models.Intervention.objects.get_or_create(
                            label = intervention_label,
                            slug = intervention_slug,
                            arm_group_label = arm_group_label,
                            description = description,
                            other_name = other_name,
                            intervention_type = intervention_type,
                            intervention_name = intervention_name,
                            )
            intervention.provenances.add(provenance)
            intervention.save()
            trial.interventions.add(intervention)
        
        #
        # 11) secondary_outcome
        #
        
        secondary_outcome_results = p.findall('secondary_outcome')
        for secondary_outcome_result in secondary_outcome_results:
            secondary_outcome_hasharray = ['Outcome']
            safety_issue = ''
            safety_issue_result = secondary_outcome_result.findall('safety_issue')
            if safety_issue_result:
                safety_issue = safety_issue_result[0].text
                secondary_outcome_hasharray.append(safety_issue_result[0].text + '(safety_issue)')
            measure = ''
            measure_result = secondary_outcome_result.findall('measure')
            if measure_result:
                measure = measure_result[0].text
                secondary_outcome_hasharray.append(measure_result[0].text + '(measure)')
            description = ''
            description_result = secondary_outcome_result.findall('description')
            if description_result:
                description = description_result[0].text
                secondary_outcome_hasharray.append(description_result[0].text + '(description)')
            time_frame = ''
            time_frame_result = secondary_outcome_result.findall('time_frame')
            if time_frame_result:
                time_frame = time_frame_result[0].text
                secondary_outcome_hasharray.append(time_frame_result[0].text + '(time_frame)')
            secondary_outcome_slug = hashlib.md5(str(set(secondary_outcome_hasharray))).hexdigest()
            #secondary_outcome_name = ...
            secondary_outcome, created = models.Outcome.objects.get_or_create(
                            #label = secondary_outcome_name,
                            label = secondary_outcome_slug,
                            slug = secondary_outcome_slug,
                            safety_issue = safety_issue,
                            measure = measure,
                            description = description,
                            time_frame = time_frame,
                            )
            secondary_outcome.provenances.add(provenance)
            secondary_outcome.save()
            trial.secondary_outcomes.add(secondary_outcome)
        
        #
        # 12) Keyword
        #
        
        keyword_results = p.findall('keyword')
        for keyword_result in keyword_results:
            keyword_name = keyword_result.text
            keyword_slug = slugify(keyword_name)
            if len(keyword_slug)>127:
                keyword_slug = hashlib.md5(keyword_slug).hexdigest()
            try:
                keyword, created = models.Keyword.objects.get_or_create(
                            label = keyword_name,
                            slug = keyword_slug,
                            )
            except:
                keyword = models.Keyword.objects.get(
                            slug = keyword_slug,
                            )
            keyword.provenances.add(provenance)
            keyword.save()
            trial.keywords.add(keyword) 
        
        #
        # 13) overall_contact_backup
        #
        
        overall_contact_backup_results = p.findall('overall_contact_backup')
        if overall_contact_backup_results:
            overall_contact_backup_result = overall_contact_backup_results[0]
            overall_contact_backup_hasharray = ['Contact']
            phone_ext = ''
            phone_ext_result = overall_contact_backup_result.findall('phone_ext')
            if phone_ext_result:
                phone_ext = phone_ext_result[0].text
                overall_contact_backup_hasharray.append(phone_ext_result[0].text + '(phone_ext)')
            
            phone = ''
            phone_result = overall_contact_backup_result.findall('phone')
            if phone_result:
                phone = phone_result[0].text
                overall_contact_backup_hasharray.append(phone_result[0].text + '(phone)')
            
            email = ''
            email_result = overall_contact_backup_result.findall('email')
            if email_result:
                email = email_result[0].text
                overall_contact_backup_hasharray.append(email_result[0].text + '(email)')
            
            last_name = ''
            last_name_result = overall_contact_backup_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_contact_backup_hasharray.append(last_name_result[0].text + '(last_name)')
            overall_contact_backup_slug = hashlib.md5(str(set(overall_contact_backup_hasharray))).hexdigest()
            overall_contact_backup_name = overall_contact_backup_slug
            if last_name:
                    overall_contact_backup_name = last_name + ' (Contact)'
            overall_contact_backup, created = models.Contact.objects.get_or_create(
                            label = overall_contact_backup_name,
                            slug = overall_contact_backup_slug,
                            phone_ext = phone_ext,
                            phone = phone,
                            email = email,
                            last_name = last_name,
                            )
            overall_contact_backup.provenances.add(provenance)

            overall_contact_backup.save()
            trial.overall_contact_backup = overall_contact_backup
        
        #
        # 14) condition
        #
        
        condition_results = p.findall('condition')
        for condition_result in condition_results:
            condition_name = condition_result.text
            condition_slug = slugify(condition_name)
            if len(condition_slug)>127:
                condition_slug = hashlib.md5(condition_slug).hexdigest()
            try:
                condition, created = models.Condition.objects.get_or_create(
                            label = condition_name,
                            slug = condition_slug,
                            )
            except:
                condition = models.Condition.objects.get(
                            slug = condition_slug,
                            )
            
            condition.provenances.add(provenance)
            condition.save()
            trial.conditions.add(condition) 
        
        #
        # 15) reference
        #
        
        reference = p.findall('reference')
        for reference in reference:
            reference_hasharray = ['Reference']
            citation = ''
            citation_result = reference.findall('citation')
            if citation_result:
                citation = citation_result[0].text
                reference_hasharray.append(citation_result[0].text + '(citation)')
            PMID = ''
            PMID_result = reference.findall('PMID')
            if PMID_result:
                PMID = PMID_result[0].text
                reference_hasharray.append(PMID_result[0].text + '(PMID)')
            reference_slug = hashlib.md5(str(set(reference_hasharray))).hexdigest()
            reference_name = reference_slug
            if PMID:
                reference_name = 'PMID:' + PMID
            reference, created = models.Reference.objects.get_or_create(
                            label = reference_name,
                            #slug = reference_slug,
                            citation = citation,
                            PMID = PMID,
                            )
            reference.provenances.add(provenance)

            reference.save()
            trial.references.add(reference)
        
        #
        # 16) primary_outcome
        #
        
        primary_outcome_results = p.findall('primary_outcome')
        for primary_outcome_result in primary_outcome_results:
            primary_outcome_hasharray = ['Outcome']
            safety_issue = ''
            safety_issue_result = primary_outcome_result.findall('safety_issue')
            if safety_issue_result:
                safety_issue = safety_issue_result[0].text
                primary_outcome_hasharray.append(safety_issue_result[0].text + '(safety_issue)')
            measure = ''
            measure_result = primary_outcome_result.findall('measure')
            if measure_result:
                measure = measure_result[0].text
                primary_outcome_hasharray.append(measure_result[0].text + '(measure)')
            description = ''
            description_result = primary_outcome_result.findall('description')
            if description_result:
                description = description_result[0].text
                primary_outcome_hasharray.append(description_result[0].text + '(description)')
            time_frame = ''
            time_frame_result = primary_outcome_result.findall('time_frame')
            if time_frame_result:
                time_frame = time_frame_result[0].text
                primary_outcome_hasharray.append(time_frame_result[0].text + '(time_frame)')
            primary_outcome_slug = hashlib.md5(str(set(primary_outcome_hasharray))).hexdigest()
            #primary_outcome_name = ...
            primary_outcome, created = models.Outcome.objects.get_or_create(
                            #label = primary_outcome_name,
                            label = primary_outcome_slug,
                            slug = primary_outcome_slug,
                            safety_issue = safety_issue,
                            measure = measure,
                            description = description,
                            time_frame = time_frame,
                            )
            primary_outcome.provenances.add(provenance)
            primary_outcome.save()
            trial.primary_outcomes.add(primary_outcome)
        
        #
        # 17) sponsors
        #
        
        sponsor_group_hasharray = ['Sponsor Group']

        sponsor_group_results = p.findall('sponsors')
        for sponsor_group_result in sponsor_group_results:

            collaborator_list = []
            collaborator_results = sponsor_group_result.findall('collaborator')
            for collaborator_result in collaborator_results:
                collaborator_hasharray = ['Sponsor']
                agency_class = ''
                agency_class_result = collaborator_result.findall('agency_class')
                if agency_class_result:
                    agency_class = agency_class_result[0].text
                    collaborator_hasharray.append(agency_class + '(agency_class)')
                agency = ''
                agency_result = collaborator_result.findall('agency')
                if agency_result:
                    agency = agency_result[0].text
                    collaborator_hasharray.append(agency + '(agency)')
                collaborator_slug = hashlib.md5(str(set(collaborator_hasharray))).hexdigest()
                if agency_result:
                    collaborator_name = agency + ' (Sponsor)' 
                collaborator, created = models.Sponsor.objects.get_or_create(
                                label = collaborator_name,
                                slug = collaborator_slug,
                                agency_class = agency_class,
                                agency = agency,
                                )
                collaborator.provenances.add(provenance)
    
                sponsor_group_hasharray.append(collaborator_slug)
                collaborator.save()
                collaborator_list.append(collaborator)
                #trial.collaborators.add(collaborator)
    
            lead_sponsor_results = sponsor_group_result.findall('lead_sponsor')
            if lead_sponsor_results:
                lead_sponsor_result = lead_sponsor_results[0]
                lead_sponsor_hasharray = ['Sponsor']
                agency_class = ''
                agency_class_result = lead_sponsor_result.findall('agency_class')
                if agency_class_result:
                    agency_class = agency_class_result[0].text
                    lead_sponsor_hasharray.append(agency_class + '(agency_class)')
                agency = ''
                agency_result = lead_sponsor_result.findall('agency')
                if agency_result:
                    agency = agency_result[0].text
                    lead_sponsor_hasharray.append(agency + '(agency)')
                lead_sponsor_slug = hashlib.md5(str(set(lead_sponsor_hasharray))).hexdigest()
                if agency_result:
                    lead_sponsor_name = agency + ' (Sponsor)'

                lead_sponsor, created = models.Sponsor.objects.get_or_create(
                                label = lead_sponsor_name,
                                slug = lead_sponsor_slug,
                                agency_class = agency_class,
                                agency = agency,
                                )
                lead_sponsor.provenances.add(provenance)
                sponsor_group_hasharray.append(lead_sponsor_slug)
                lead_sponsor.save()
                #trial.lead_sponsor_group.add(lead_sponsor)
            
            
            
            sponsor_group_slug = hashlib.md5(str(set(sponsor_group_hasharray))).hexdigest()
            #sponsor_group_name = ...
            sponsor_group, created = models.Sponsor_group.objects.get_or_create(
                            #label = sponsor_group_name,
                            label = sponsor_group_slug,
                            slug = sponsor_group_slug,
                            )
            sponsor_group.lead_sponsor = lead_sponsor
            sponsor_group.provenances.add(provenance)

            for s in collaborator_list:
                sponsor_group.collaborators.add(s)

            sponsor_group.save()
            trial.sponsor_group = sponsor_group
        
        #
        # 18) oversight_info
        #

        oversight_info_results = p.findall('oversight_info')
        if oversight_info_results:
            oversight_info_result = oversight_info_results[0]
            oversight_info_hasharray = ['Oversight_info']
            authority = ''
            authority_result = oversight_info_result.findall('authority')
            if authority_result:
                authority = authority_result[0].text
                oversight_info_hasharray.append(authority + '(authority)')
            has_dmc = ''
            has_dmc_result = oversight_info_result.findall('has_dmc')
            if has_dmc_result:
                has_dmc = has_dmc_result[0].text
                oversight_info_hasharray.append(has_dmc + '(has_dmc)')
            oversight_info_slug = hashlib.md5(str(set(oversight_info_hasharray))).hexdigest()
            if authority!='':
                oversight_info_name = authority + ' (Oversight_info)'
            try:
                oversight_info, created = models.Oversight_info.objects.get_or_create(
                            label = oversight_info_name,
                            slug = oversight_info_slug,
                            authority = authority,
                            has_dmc = has_dmc,
                            )
            except:
                oversight_info = models.Oversight_info.objects.get(
                            authority = authority,
                            has_dmc = has_dmc,
                            )
            oversight_info.provenances.add(provenance)
            oversight_info.save()
            trial.oversight_info = oversight_info
        
        #
        # 19) removed_countries_country
        #
        
        removed_countries_results = p.findall('removed_countries')
        for removed_countries_result in removed_countries_results:
            country_results = removed_countries_result.findall('country')
            for country_result in country_results:
                country_name = country_result.text
                if slugify(country_name)=='':
                        country_name = 'N/A'
                country, created = models.Country.objects.get_or_create(
                                label = country_name,
                                country_name = country_name,
                                )
                country.provenances.add(provenance)
                country.save()
                trial.removed_countries.add(country)
        
        #
        # 20) eligibility
        #
        
        eligibility_results = p.findall('eligibility')
        for eligibility_result in eligibility_results:
            eligibility_hasharray = ['Eligibility']
            criteria_textblock = ''
            criteria_textblock_result = eligibility_result.findall('criteria/textblock')
            if criteria_textblock_result:
                criteria_textblock = criteria_textblock_result[0].text
                eligibility_hasharray.append(criteria_textblock)
            maximum_age = ''
            maximum_age_result = eligibility_result.findall('maximum_age')
            if maximum_age_result:
                maximum_age = maximum_age_result[0].text
                eligibility_hasharray.append(maximum_age + '(maximum_age)')
            healthy_volunteers = ''
            healthy_volunteers_result = eligibility_result.findall('healthy_volunteers')
            if healthy_volunteers_result:
                healthy_volunteers = healthy_volunteers_result[0].text
                eligibility_hasharray.append(healthy_volunteers + '(healthy_volunteers)')
            study_pop_textblock = ''
            study_pop_textblock_result = eligibility_result.findall('study_pop/textblock')
            if study_pop_textblock_result:
                study_pop_textblock = study_pop_textblock_result[0].text
                eligibility_hasharray.append(study_pop_textblock + '(study_pop/textblock)')
            minimum_age = ''
            minimum_age_result = eligibility_result.findall('minimum_age')
            if minimum_age_result:
                minimum_age = minimum_age_result[0].text
                eligibility_hasharray.append(minimum_age + '(minimum_age)')
            gender = ''
            gender_result = eligibility_result.findall('gender')
            if gender_result:
                gender = gender_result[0].text
                eligibility_hasharray.append(gender + '(gender)')
            sampling_method = ''
            sampling_method_result = eligibility_result.findall('sampling_method')
            if sampling_method_result:
                sampling_method = sampling_method_result[0].text
                eligibility_hasharray.append(sampling_method + '(sampling_method)')
            eligibility_slug = hashlib.md5(str(set(eligibility_hasharray))).hexdigest()
            #eligibility_name = ...
            eligibility, created = models.Eligibility.objects.get_or_create(
                            #label = eligibility_name,
                            label = eligibility_slug,
                            slug = eligibility_slug,
                            criteria = criteria_textblock,
                            maximum_age = maximum_age,
                            healthy_volunteers = healthy_volunteers,
                            study_pop = study_pop_textblock,
                            minimum_age = minimum_age,
                            gender = gender,
                            sampling_method = sampling_method,
                            )
            eligibility.provenances.add(provenance)
            eligibility.save()
            trial.eligibility = eligibility
        
        #
        # 21) overall_official
        #
        
        overall_official_results = p.findall('overall_official')
        for overall_official_result in overall_official_results:
            overall_official_hasharray = ['Overall Official']
            last_name = ''
            last_name_result = overall_official_result.findall('last_name')
            if last_name_result:
                last_name = last_name_result[0].text
                overall_official_hasharray.append(last_name_result[0].text + '(last_name)')
            role = ''
            role_result = overall_official_result.findall('role')
            if role_result:
                role = role_result[0].text
                overall_official_hasharray.append(role_result[0].text + '(role)')
            affiliation = ''
            affiliation_result = overall_official_result.findall('affiliation')
            if affiliation_result:
                affiliation = affiliation_result[0].text
                overall_official_hasharray.append(affiliation_result[0].text + '(affiliation)')
            overall_official_slug = hashlib.md5(str(set(overall_official_hasharray))).hexdigest()
            #overall_official_name = ...
            overall_official, created = models.Overall_official.objects.get_or_create(
                            #label = overall_official_name,
                            label = overall_official_slug,
                            slug = overall_official_slug,
                            last_name = last_name,
                            role = role,
                            affiliation = affiliation,
                            )
            overall_official.provenances.add(provenance)
            overall_official.save()
            trial.overall_officials.add(overall_official)
        
        
        trial.save()

    provenance.signature = signature
    provenance.save()
    return provenance


def download_url(url, size_limit):
    """Download the url and save it to local file."""
    try:
        request = urllib2.urlopen(url)

        # Check if file size exceeds limit. Since this is a remote URL, and we
        # cannot determine its size (HTTP header size is optional and
        # unreliable), we first read the limit, and then read one more byte
        # to determine if it exceeds the limit.
        content = request.read(size_limit)
        if request.read(1):
            raise FileSizeLimitExceededException(size_limit)
        request.close()
        return content
    except urllib2.URLError, e:
        raise UrlException(e)
