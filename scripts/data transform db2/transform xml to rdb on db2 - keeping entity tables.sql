/*
 * May need the following
 */
 connect reset;
 connect to FORXML ;
  update db cfg using applheapsz 60000;
  update db cfg using app_ctl_heap_sz 60000;
  update db cfg using LOGFILSIZ 60000;
 connect reset;
connect to FORXML ;

/*
 * May need to RESTART the DB2 instance after the above changes
 * Also, need to create BUFFERSPACE and TABLESPACE with pagesize 16 and 32K both USER and TEMP categories. This can be done in DB2 Control Center
 */

/*
 * Base TABLE:
 */


DROP table admin.cttrials;
CREATE table admin.cttrials (
	id	CHAR(11) NOT NULL,
	download_date 		VARCHAR(100),
	link_text 		VARCHAR(200),
	url 			VARCHAR(150),
	org_study_id 		VARCHAR(50),
	nct_id 			VARCHAR(50),
	brief_title 		VARCHAR(600),
	acronym 		VARCHAR(50),
	official_title 		VARCHAR(600),
	lead_sponsor_agency	VARCHAR(150),
	source 			VARCHAR(150),
	has_dmc 		VARCHAR(100),
	overall_status 		VARCHAR(100),
	why_stopped 		VARCHAR(300),
	phase 			VARCHAR(100),
	study_type 		VARCHAR(200),
	study_design 		VARCHAR(200),
	number_of_arms 		INTEGER,
	number_of_groups 	INTEGER,
	enrollment 		INTEGER,
	biospec_retention 	VARCHAR(200),
	eligibility_study_pop 		VARCHAR(2000),
	eligibility_sampling_method	VARCHAR(200),
	eligibility_gender 		VARCHAR(20),
	eligibility_minimum_age 	VARCHAR(20),
	eligibility_maximum_age 	VARCHAR(20),
	eligibility_healthy_volunteers 	VARCHAR(200),
	overall_contact_first_name 		VARCHAR(100),
	overall_contact_middle_name 		VARCHAR(50),
	overall_contact_last_name 		VARCHAR(150),
	overall_contact_degrees 		VARCHAR(200),
	overall_contact_phone 			VARCHAR(100),
	overall_contact_phone_ext 		VARCHAR(100),
	overall_contact_email 			VARCHAR(200),
	start_date 			VARCHAR(100),
	end_date  			VARCHAR(100),
	primary_completion_date 	VARCHAR(100),
	verification_date 		VARCHAR(100),
	lastchanged_date 		VARCHAR(100),
	firstreceived_date 		VARCHAR(100),
	PRIMARY KEY(id)
);

INSERT into admin.cttrials
SELECT CT.id, X.*
FROM ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study' PASSING BY REF trial AS "doc"
       COLUMNS
	download_date 		VARCHAR(100) 	PATH './required_header/download_date',
	link_text 			VARCHAR(200) 	PATH './required_header/link_text',
	url 				VARCHAR(150) 	PATH './required_header/url',
	org_study_id 		VARCHAR(50) 	PATH './id_info/org_study_id',
	nct_id 				VARCHAR(50) 	PATH './id_info/nct_id',
	brief_title 		VARCHAR(600)	PATH './brief_title',
	acronym 			VARCHAR(50) 	PATH './acronym',
	official_title 		VARCHAR(600) 	PATH './official_title',
	lead_sponsor_agency	VARCHAR(150) 	PATH './sponsors/lead_sponsor/agency',
	source 				VARCHAR(150) 	PATH './source',
	has_dmc 			VARCHAR(100) 	PATH './oversight_info/has_dmc',
	overall_status 		VARCHAR(100) 	PATH './overall_status',
	why_stopped 		VARCHAR(300) 	PATH './why_stopped',
	phase 				VARCHAR(100) 	PATH './phase',
	study_type 			VARCHAR(200) 	PATH './study_type',
	study_design 		VARCHAR(200) 	PATH './study_design',
	number_of_arms 		INTEGER 	PATH './number_of_arms',
	number_of_groups 	INTEGER 	PATH './number_of_groups',
	enrollment 			INTEGER 	PATH './enrollment',
	biospec_retention 	VARCHAR(200) 	PATH './biospec_retention',
	eligibility_study_pop 		VARCHAR(2000) 	PATH './eligibility/study_pop',
	eligibility_sampling_method	VARCHAR(200)	PATH './eligibility/sampling_method',
	eligibility_gender 			VARCHAR(20) 	PATH './eligibility/gender',
	eligibility_minimum_age 	VARCHAR(20) 	PATH './eligibility/minimum_age',
	eligibility_maximum_age 	VARCHAR(20) 	PATH './eligibility/maximum_age',
	eligibility_healthy_volunteers 	VARCHAR(200) 	PATH './eligibility/healthy_volunteers',
	overall_contact_first_name 		VARCHAR(100)	PATH './overall_contact/first_name',
	overall_contact_middle_name 	VARCHAR(50)	PATH './overall_contact/middle_name',
	overall_contact_last_name 		VARCHAR(150)	PATH './overall_contact/last_name',
	overall_contact_degrees 		VARCHAR(200)	PATH './overall_contact/degrees',
	overall_contact_phone 			VARCHAR(100)	PATH './overall_contact/phone',
	overall_contact_phone_ext 		VARCHAR(100)	PATH './overall_contact/phone_ext',
	overall_contact_email 			VARCHAR(200)	PATH './overall_contact/email',
	start_date 					VARCHAR(100)	PATH './start_date',
	end_date  					VARCHAR(100)	PATH './end_date',
	primary_completion_date 	VARCHAR(100)	PATH './primary_completion_date',
	verification_date 			VARCHAR(100)	PATH './verification_date',
	lastchanged_date 			VARCHAR(100)	PATH './lastchanged_date',
	firstreceived_date 			VARCHAR(100)	PATH './firstreceived_date'
           ) AS X;



/*
 *  Text columns:
 */

DROP table admin.cttrials_summary;
CREATE table admin.cttrials_summary (
	id	CHAR(11) NOT NULL,
	brief_summary 		VARCHAR(30000),
	PRIMARY KEY(id)
);

DROP table admin.cttrials_description;
CREATE table admin.cttrials_description (
	id	CHAR(11) NOT NULL,
	detailed_description 	CLOB(90000),
	PRIMARY KEY(id)
);

DROP table admin.cttrials_biospec;
CREATE table admin.cttrials_biospec (
	id	CHAR(11) NOT NULL,
	biospec_descr 		VARCHAR(30000),
	PRIMARY KEY(id)
);

DROP table admin.cttrials_criteria;
CREATE table admin.cttrials_criteria (
	id	CHAR(11) NOT NULL,
	eligibility_criteria		VARCHAR(30000),
	PRIMARY KEY(id)
);

INSERT into admin.cttrials_summary
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study' PASSING BY REF trial AS "doc"
       COLUMNS
		brief_summary 		VARCHAR(30000) 	PATH './brief_summary'
           ) AS X;

INSERT into admin.cttrials_description
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study' PASSING BY REF trial AS "doc"
       COLUMNS
		detailed_description 	CLOB(100000)	PATH './detailed_description'
           ) AS X;
           
INSERT into admin.cttrials_biospec
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study' PASSING BY REF trial AS "doc"
       COLUMNS
		biospec_descr 		VARCHAR(30000) 	PATH './biospec_descr'
           ) AS X;
           
INSERT into admin.cttrials_criteria
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study' PASSING BY REF trial AS "doc"
       COLUMNS
		eligibility_criteria		VARCHAR(30000)	PATH './eligibility/criteria'
           ) AS X;
           
           
           

           
           
           
           
/*
 *  Multi-valued columns
 */

/*
 *  Secondary IDs:
 */
 
DROP table admin.cttrials2secid;
CREATE table admin.cttrials2secid(
	ID char(11) NOT NULL,
	secondary_id 	VARCHAR(100)
);

INSERT into admin.cttrials2secid
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/id_info/secondary_id' PASSING BY REF trial AS "doc"
       COLUMNS
        secondary_id 	VARCHAR(100) PATH '.'
     ) AS X;


/*
 *  NCT_aliases:
 */
DROP table admin.cttrials2nctalias;
CREATE table admin.cttrials2nctalias(
	ID char(11) NOT NULL,
	nct_alias 	VARCHAR(100)
);

INSERT into admin.cttrials2nctalias
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/id_info/nct_alias' PASSING BY REF trial AS "doc"
       COLUMNS
	nct_alias 	VARCHAR(100) PATH '.'
     ) AS X;
     
     
/*
 *  collaborator_agency:
 */
DROP table admin.cttrials2collabagency;
CREATE table admin.cttrials2collabagency(
	ID char(11) NOT NULL,
	collaborator_agency 	VARCHAR(300)
);

INSERT into admin.cttrials2collabagency
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/sponsors/collaborator/agency' PASSING BY REF trial AS "doc"
       COLUMNS
	collaborator_agency 	VARCHAR(300) PATH '.'
     ) AS X;
     
/*
 *  oversight_info_authority:
 */
DROP table admin.cttrials2oversight;
CREATE table admin.cttrials2oversight(
	ID char(11) NOT NULL,
	oversight_info_authority 	VARCHAR(300)
);

INSERT into admin.cttrials2oversight
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/oversight_info/authority' PASSING BY REF trial AS "doc"
       COLUMNS
	oversight_info_authority 	VARCHAR(300) PATH '.'
     ) AS X;
     
     
/*
 *  condition:
 */
DROP table admin.cttrials2condition;
CREATE table admin.cttrials2condition(
	ID char(11) NOT NULL,
	condition 	VARCHAR(200)
);

INSERT into admin.cttrials2condition
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/condition' PASSING BY REF trial AS "doc"
       COLUMNS
	condition 	VARCHAR(200) PATH '.'
     ) AS X;
     
     
/*
 *  primary_outcomes:
 */
DROP table admin.cttrials2primary_outcomes;
CREATE table admin.cttrials2primary_outcomes(
	ID char(11) NOT NULL,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10) 
);


INSERT into admin.cttrials2primary_outcomes
WITH pp (id, primary_outcome) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/primary_outcome' PASSING BY REF trial AS "doc"
       COLUMNS
	primary_outcome 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF primary_outcome AS "doc"
       COLUMNS
	measure 	VARCHAR(400) 	PATH './measure',
	time_frame 	VARCHAR(300) 	PATH './time_frame',
	safety_issue 	VARCHAR(10) 	PATH './safety_issue'
     ) AS Y;
     
     
     



/*
 *  secondary_outcomes:
 */
DROP table admin.cttrials2secondary_outcomes;
CREATE table admin.cttrials2secondary_outcomes(
	ID char(11) NOT NULL,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10) 
);


INSERT into admin.cttrials2secondary_outcomes
WITH pp (id, secondary_outcome) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/secondary_outcome' PASSING BY REF trial AS "doc"
       COLUMNS
	secondary_outcome 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF secondary_outcome AS "doc"
       COLUMNS
	measure 	VARCHAR(400) 	PATH './measure',
	time_frame 	VARCHAR(300) 	PATH './time_frame',
	safety_issue 	VARCHAR(10) 	PATH './safety_issue'
     ) AS Y;
     
     
     
     
     


/*
 *  arm_group:
 */
DROP table admin.cttrials2arm_group;
CREATE table admin.cttrials2arm_group(
	ID char(11) NOT NULL,
	arm_group_label 	VARCHAR(100),
	arm_group_type  	VARCHAR(100),
	description		VARCHAR(2000)
);

INSERT into admin.cttrials2arm_group
WITH pp (id, arm_group) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/arm_group' PASSING BY REF trial AS "doc"
       COLUMNS
	arm_group 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF arm_group AS "doc"
       COLUMNS
	arm_group_label 	VARCHAR(100) 	PATH './arm_group_label',
	arm_group_type  	VARCHAR(100) 	PATH './arm_group_type ',
	description 	VARCHAR(2000) 	PATH './description'
     ) AS Y;




/*
 *  intervention:
 */
DROP table admin.cttrials2intervention;
CREATE table admin.cttrials2intervention(
	ID char(11) NOT NULL,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 	VARCHAR(2000)
);

INSERT into admin.cttrials2intervention
WITH pp (id, intervention) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/intervention' PASSING BY REF trial AS "doc"
       COLUMNS
	intervention 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF intervention AS "doc"
       COLUMNS
	intervention_type 	VARCHAR(100) 	PATH './intervention_type',
	intervention_name 	VARCHAR(200) 	PATH './intervention_name',
	description 	VARCHAR(2000) 	PATH './description'
     ) AS Y;

/*
 *  intervention2arm:
 */
DROP table admin.ctintervention2arm;
CREATE table admin.ctintervention2arm(
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 	VARCHAR(2000),
	arm_group_label VARCHAR(100)
);

INSERT into admin.ctintervention2arm
WITH pp (id, intervention) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/intervention' PASSING BY REF trial AS "doc"
       COLUMNS
	intervention 	XML PATH '.'
     ) AS X
)
SELECT Y.*, Z.*
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF intervention AS "doc"
       COLUMNS
	intervention_type 	VARCHAR(100) 	PATH './intervention_type',
	intervention_name 	VARCHAR(200) 	PATH './intervention_name',
	description 	VARCHAR(2000) 	PATH './description'
     ) AS Y, 
     XMLTABLE('$doc/arm_group_label' PASSING BY REF intervention AS "doc"
       COLUMNS
	arm_group_label 	VARCHAR(100) 	PATH '.'
     ) AS Z;




/*
 *  internvention2other_name
 */
DROP table admin.ctintervention2other_name;
CREATE table admin.ctintervention2other_name(
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 	VARCHAR(2000),
	other_name 	VARCHAR(200) 
);

INSERT into admin.ctintervention2other_name
WITH pp (id, intervention) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/intervention' PASSING BY REF trial AS "doc"
       COLUMNS
	intervention 	XML PATH '.'
     ) AS X
)
SELECT Y.*, Z.*
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF intervention AS "doc"
       COLUMNS
	intervention_type 	VARCHAR(100) 	PATH './intervention_type',
	intervention_name 	VARCHAR(200) 	PATH './intervention_name',
	description 	VARCHAR(2000) 	PATH './description'
     ) AS Y,
     XMLTABLE('$doc/other_name' PASSING BY REF intervention AS "doc"
       COLUMNS
	other_name 	VARCHAR(200) 	PATH '.'
     ) AS Z;

   
     
     
     
     
     
     
     
     
/*
 *  trials2overall_official:
 */
DROP table admin.cttrials2overall_official;
CREATE table admin.cttrials2overall_official(
	ID char(11) NOT NULL,
	first_name 		VARCHAR(100),
	middle_name 		VARCHAR(100),
	last_name 		VARCHAR(200),
	degrees 		VARCHAR(100),
	role 			VARCHAR(200),
	affiliation 		VARCHAR(300)
);

INSERT into admin.cttrials2overall_official
WITH pp (id, overall_official) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/overall_official' PASSING BY REF trial AS "doc"
       COLUMNS
	overall_official 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF overall_official AS "doc"
       COLUMNS
	first_name 		VARCHAR(100)	PATH './first_name',
	middle_name 		VARCHAR(100)	PATH './middle_name',
	last_name 		VARCHAR(200)	PATH './last_name',
	degrees 		VARCHAR(100)	PATH './degrees',
	role 			VARCHAR(200)	PATH './role',
	affiliation 		VARCHAR(300)	PATH './affiliation'
     ) AS Y;










/*
 *  trials2location:
 */
DROP table admin.cttrials2location;
CREATE table admin.cttrials2location(
	ID char(11) NOT NULL,
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200), 
	facility_address_state 		VARCHAR(200), 
	facility_address_zip 		VARCHAR(200),
	facility_address_country 	VARCHAR(200),
	status 				VARCHAR(300),
	contact_first_name 		VARCHAR(100),
	contact_middle_name 		VARCHAR(100),
	contact_last_name 		VARCHAR(300), 
	contact_degrees 		VARCHAR(100), 
	contact_phone 			VARCHAR(100), 
	contact_phone_ext 		VARCHAR(100),
	contact_email 			VARCHAR(300),
	contact_backup_first_name 	VARCHAR(100),
	contact_backup_middle_name 	VARCHAR(100),
	contact_backup_last_name 	VARCHAR(300), 
	contact_backup_degrees 		VARCHAR(100), 
	contact_backup_phone 		VARCHAR(100), 
	contact_backup_phone_ext 	VARCHAR(100), 
	contact_backup_email 		VARCHAR(100)
);

INSERT into admin.cttrials2location
WITH pp (id, location) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/location' PASSING BY REF trial AS "doc"
       COLUMNS
	location 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF location AS "doc"
       COLUMNS
	facility_name 			VARCHAR(400)	PATH './facility/name',
	facility_address_city 		VARCHAR(200)	PATH './facility/address/city', 
	facility_address_state 		VARCHAR(200)	PATH './facility/address/state', 
	facility_address_zip 		VARCHAR(200)	PATH './facility/address/zip',
	facility_address_country 	VARCHAR(200)	PATH './facility/address/country',
	status 				VARCHAR(300)	PATH './status',
	contact_first_name 		VARCHAR(100)	PATH './contact/first_name',
	contact_middle_name 		VARCHAR(100)	PATH './contact/middle_name ',
	contact_last_name 		VARCHAR(300)	PATH './contact/last_name', 
	contact_degrees 		VARCHAR(100)	PATH './contact/degrees', 
	contact_phone 			VARCHAR(100)	PATH './contact/phone', 
	contact_phone_ext 		VARCHAR(100)	PATH './contact/phone_ext',
	contact_email 			VARCHAR(300)	PATH './contact/email',
	contact_backup_first_name 	VARCHAR(100)	PATH './contact_backup/first_name',
	contact_backup_middle_name 	VARCHAR(100)	PATH './contact_backup/middle_name',
	contact_backup_last_name 	VARCHAR(300)	PATH './contact_backup/last_name', 
	contact_backup_degrees 		VARCHAR(100)	PATH './contact_backup/degrees', 
	contact_backup_phone 		VARCHAR(100)	PATH './contact_backup/phone', 
	contact_backup_phone_ext 	VARCHAR(100)	PATH './contact_backup/phone_ext', 
	contact_backup_email 		VARCHAR(100)	PATH './contact_backup/email'
     ) AS Y;

	



/*
 *  location2investigator:
 */
DROP table admin.ctlocation2investigator;
CREATE table admin.ctlocation2investigator(
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200),
	facility_address_state 		VARCHAR(200),
	facility_address_zip 		VARCHAR(100),
	facility_address_country 	VARCHAR(100),
	first_name 	VARCHAR(100),
	middle_name 	VARCHAR(100),
	last_name 	VARCHAR(100),
	degrees 	VARCHAR(100),
	role 		VARCHAR(100)
);


INSERT into admin.ctlocation2investigator
WITH pp (id, location) AS
(
SELECT CT.id, X.*
from ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/location' PASSING BY REF trial AS "doc"
       COLUMNS
	location 	XML PATH '.'
     ) AS X
),
ppp (facility_name,facility_address_city,facility_address_state,facility_address_zip,facility_address_country, investigator) AS
(
SELECT Y.*, Z.*
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF location AS "doc"
       COLUMNS
	facility_name 			VARCHAR(400)	PATH './facility/name',
	facility_address_city 		VARCHAR(200)	PATH './facility/address/city', 
	facility_address_state 		VARCHAR(200)	PATH './facility/address/state', 
	facility_address_zip 		VARCHAR(100)	PATH './facility/address/zip',
	facility_address_country 	VARCHAR(100)	PATH './facility/address/country'
     ) AS Y, 
     XMLTABLE('$doc/investigator' PASSING BY REF location AS "doc"
       COLUMNS
	investigator 	XML 	PATH '.'
     ) AS Z
)
SELECT facility_name,facility_address_city,facility_address_state,facility_address_zip,facility_address_country, W.*
FROM ppp p2,
     XMLTABLE('$doc' PASSING BY REF investigator AS "doc"
       COLUMNS
	first_name 	VARCHAR(100)	PATH './first_name',
	middle_name 	VARCHAR(100)	PATH './middle_name ',
	last_name 	VARCHAR(100)	PATH './last_name ',
	degrees 	VARCHAR(100)	PATH './degrees ',
	role 		VARCHAR(100)	PATH './role '
     ) AS W;







/*
 *  trials2reference:
 */
DROP table admin.cttrials2reference;
CREATE table admin.cttrials2reference(
	ID char(11) NOT NULL,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);

INSERT into admin.cttrials2reference
WITH pp (id, reference) AS
(
SELECT CT.id, X.*
FROM ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/reference' PASSING BY REF trial AS "doc"
       COLUMNS
	reference 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF reference AS "doc"
       COLUMNS
	citation 			VARCHAR(10000)	PATH './citation',
	PMID 				VARCHAR(100)	PATH './PMID'
     ) AS Y;





/*
 *  trials2results_reference:
 */
DROP table admin.cttrials2results_reference;
CREATE table admin.cttrials2results_reference(
	ID char(11) NOT NULL,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);

INSERT into admin.cttrials2results_reference
WITH pp (id, results_reference) AS
(
SELECT CT.id, X.*
FROM ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/results_reference' PASSING BY REF trial AS "doc"
       COLUMNS
	results_reference 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF results_reference AS "doc"
       COLUMNS
	citation 			VARCHAR(10000)	PATH './citation',
	PMID 				VARCHAR(100)	PATH './PMID'
     ) AS Y;





/*
 *  trials2link:
 */
DROP table admin.cttrials2link;
CREATE table admin.cttrials2link(
	ID char(11) NOT NULL,
	url 				VARCHAR(400), 
	description 			VARCHAR(2000)
);

INSERT into admin.cttrials2link
WITH pp (id, link) AS
(
SELECT CT.id, X.*
FROM ADMIN.CTXMLNEW AS CT,
     XMLTABLE('$doc/clinical_study/link' PASSING BY REF trial AS "doc"
       COLUMNS
	link 	XML PATH '.'
     ) AS X
)
SELECT p.id, Y.* 
FROM pp p,
     XMLTABLE('$doc' PASSING BY REF link AS "doc"
       COLUMNS
	url 				VARCHAR(400)	PATH './url', 
	description 			VARCHAR(2000)	PATH './description'
     ) AS Y



/* Entity Tables */





/*
 * Keeping intervention entity numbers
 */
 
update admin.cttrials2intervention
SET description = ''
WHERE description is null;

update admin.cttrials2intervention
SET intervention_name = ''
WHERE intervention_name is null;

update admin.cttrials2intervention
SET intervention_type = ''
WHERE intervention_type is null;


/*
 * DROP table tmp;
 * CREATE table tmp(
 * 	TID 				INTEGER not null primary key,
 * 	intervention_type 	VARCHAR(100),
 * 	intervention_name 	VARCHAR(200),
 * 	description 		VARCHAR(2000)
 * );
 * import from "C:\Users\admin\dcp-workspace\linkeddata\linkedct\data\mysql\ctintervention.csv" 
 * OF DEL MODIFIED BY DELPRIORITYCHAR CHARDEL"" COLDEL, MESSAGES "c:\Users\admin\tmp.txt" 
 * INSERT INTO tmp;
 *
 * insert into ctintervention(intervention_type, intervention_name, description) 
 * select intervention_type, intervention_name, description from TMP 
 * order by tid asc;
 */

INSERT into admin.ctintervention(intervention_type, intervention_name, description)
SELECT DISTINCT intervention_type, intervention_name, description
from admin.cttrials2intervention;

DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 		VARCHAR(2000)
);

INSERT INTO tmp
SELECT min(tid), intervention_type, intervention_name, description
FROM admin.ctintervention
GROUP BY intervention_type, intervention_name, description;

DROP table ctintervention;
CREATE table ctintervention(
	TID 			INTEGER not null generated always as identity primary key,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 		VARCHAR(2000)
);

insert into ctintervention(intervention_type, intervention_name, description) 
select intervention_type, intervention_name, description from TMP 
order by tid asc;

DROP table admin.cttrials2interventionID;
CREATE table admin.cttrials2interventionID(
    ID 			CHAR(11),
	TID 		INTEGER,
	FOREIGN KEY(ID) REFERENCES CTtrials(id)
);

INSERT into admin.cttrials2interventionID
SELECT ct.id, in.tid
from admin.cttrials2intervention ct, CTintervention in
WHERE ct.intervention_type=in.intervention_type 
	  AND ct.intervention_name = in.intervention_name
	  AND ct.description = in.description;



/*
 * Keeping condition entity numbers
 */



/*
 * DROP table tmp2;
 * CREATE table tmp2(
 * 	TID 				INTEGER not null primary key,
 * 	condition 	VARCHAR(200)
 * );
 * import from "C:\Users\admin\dcp-workspace\linkeddata\linkedct\data\mysql\ctcondition.csv" 
 * OF DEL MODIFIED BY DELPRIORITYCHAR CHARDEL"" COLDEL, MESSAGES "c:\Users\admin\tmp.txt" 
 * INSERT INTO tmp2;
 *
 * INSERT into admin.ctcondition(condition)
 * select condition from TMP2 
 * order by tid asc;
 */

INSERT into admin.ctcondition(condition)
SELECT DISTINCT condition
from admin.cttrials2condition
WHERE condition!='';

/* 
 * WHERE condition!='' AND condition NOT IN (SELECT condition FROM tmp2);
 */

DROP table tmp2;
 CREATE table tmp2(
 	TID 				INTEGER not null primary key,
 	condition 	VARCHAR(200)
 );
 
INSERT INTO tmp2
SELECT min(tid), condition
FROM admin.ctcondition
GROUP BY condition;

DROP table admin.ctcondition;
CREATE table admin.ctcondition(
	TID 				INTEGER not null generated always as identity primary key,
	condition 	VARCHAR(200)
);

insert into ctcondition(condition) 
select condition from TMP2 
order by tid asc;

DROP table admin.cttrials2conditionID;
CREATE table admin.cttrials2conditionID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2conditionID
SELECT ct.id, co.tid
from admin.cttrials2condition ct, CTcondition co
WHERE ct.condition=co.condition;




update admin.cttrials2arm_group
SET description = ''
WHERE description is null;

update admin.cttrials2arm_group
SET arm_group_type = ''
WHERE arm_group_type is null;

update admin.cttrials2arm_group
SET arm_group_label = ''
WHERE arm_group_label is null;

INSERT into admin.ctarm_group(arm_group_label, arm_group_type, description)
SELECT DISTINCT arm_group_label, arm_group_type, description
from admin.cttrials2arm_group;

DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	arm_group_label 	VARCHAR(100),
	arm_group_type  	VARCHAR(100),
	description		VARCHAR(2000)
);

INSERT INTO tmp
SELECT min(TID), arm_group_label, arm_group_type, description
FROM admin.ctarm_group
GROUP BY arm_group_label, arm_group_type, description;

DROP table admin.ctarm_group;
CREATE table admin.ctarm_group(
	TID 				INTEGER not null generated always as identity primary key,
	arm_group_label 	VARCHAR(100),
	arm_group_type  	VARCHAR(100),
	description		VARCHAR(2000)
);
INSERT into admin.ctarm_group(arm_group_label, arm_group_type, description)
SELECT arm_group_label, arm_group_type, description
from tmp
order by tid asc;



DROP table admin.cttrials2arm_groupID;
CREATE table admin.cttrials2arm_groupID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2arm_groupID
SELECT ct.id, ar.tid
from admin.cttrials2arm_group ct, CTarm_group ar
WHERE ct.arm_group_label = ar.arm_group_label AND ct.arm_group_type = ar.arm_group_type AND ct.description = ar.description;




DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	collaborator_agency 	VARCHAR(300)
);
INSERT into admin.ctcollabagency(collaborator_agency)
SELECT DISTINCT collaborator_agency
from admin.cttrials2collabagency;

INSERT INTO tmp
SELECT min(TID), collaborator_agency
FROM ctcollabagency
GROUP BY collaborator_agency;

DROP table admin.ctcollabagency;
CREATE table admin.ctcollabagency(
	TID 				INTEGER not null generated always as identity primary key,
	collaborator_agency 	VARCHAR(300)
);
INSERT into admin.ctcollabagency(collaborator_agency)
SELECT collaborator_agency
from tmp
order by tid asc;

DROP table admin.cttrials2collabagencyID;
CREATE table admin.cttrials2collabagencyID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2collabagencyID
SELECT ct.id, ar.tid
from admin.cttrials2collabagency ct, CTcollabagency ar
WHERE ct.collaborator_agency = ar.collaborator_agency;



/*
* update admin.cttrials2link
* SET url = ''
* WHERE url is null;
* 
* update admin.cttrials2link
* SET description = ''
* WHERE description is null;
* 
* DROP table admin.ctlink;
* CREATE table admin.ctlink(
* 	TID 				INTEGER not null generated always as identity primary key,
* 	url 				VARCHAR(400), 
* 	description 			VARCHAR(2000)
* );
* INSERT into admin.ctlink(url, description)
* SELECT DISTINCT url, description
* from admin.cttrials2link;
* 
* DROP table admin.cttrials2linkID;
* CREATE table admin.cttrials2linkID(
*     ID 			CHAR(11),
*     TID			INTEGER
* 
* );
* 
* INSERT into admin.cttrials2linkID
* SELECT ct.id, ar.tid
* from admin.cttrials2link ct, CTlink ar
* WHERE ct.url = ar.url AND ct.description = ar.description;
*/




update admin.cttrials2location
SET facility_name = ''
WHERE facility_name is null;

update admin.cttrials2location
SET facility_address_city = ''
WHERE facility_address_city is null;

update admin.cttrials2location
SET facility_address_state = ''
WHERE facility_address_state is null;

update admin.cttrials2location
SET facility_address_zip = ''
WHERE facility_address_zip is null;

update admin.cttrials2location
SET facility_address_country = ''
WHERE facility_address_country is null;



INSERT into admin.ctlocation(facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country)
SELECT DISTINCT facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country
from admin.cttrials2location;

DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200), 
	facility_address_state 		VARCHAR(200), 
	facility_address_zip 		VARCHAR(200),
	facility_address_country 	VARCHAR(200)
);

INSERT into tmp
SELECT min(TID), facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country
from admin.ctlocation
group by facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country;



DROP table admin.ctlocation;
CREATE table admin.ctlocation(
	TID 				INTEGER not null generated always as identity primary key,
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200), 
	facility_address_state 		VARCHAR(200), 
	facility_address_zip 		VARCHAR(200),
	facility_address_country 	VARCHAR(200)
);
INSERT into admin.ctlocation(facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country)
SELECT facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country
from tmp
order by tid asc;

DROP table admin.cttrials2locationID;
CREATE table admin.cttrials2locationID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2locationID
SELECT ct.id, ar.tid
from admin.cttrials2location ct, CTlocation ar
WHERE ct.facility_name = ar.facility_name 
	  AND ct.facility_address_city = ar.facility_address_city 
	  AND ct.facility_address_state = ar.facility_address_state 
	  AND (ct.facility_address_zip = ar.facility_address_zip OR ct.facility_address_zip is null ) 
	  AND (ct.facility_address_country = ar.facility_address_country OR ct.facility_address_country is null);
















update admin.cttrials2reference
SET citation = ''
WHERE citation is null;

update admin.cttrials2reference
SET PMID = ''
WHERE PMID is null;

DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);
INSERT into admin.ctreference(citation,PMID)
SELECT DISTINCT citation,PMID
from admin.cttrials2reference;

INSERT into tmp
SELECT min(tid), citation,PMID
from admin.ctreference
GROUP BY citation,PMID;

DROP table admin.ctreference;
CREATE table admin.ctreference(
	TID 				INTEGER not null generated always as identity primary key,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);
INSERT into admin.ctreference(citation,PMID)
SELECT citation,PMID
from tmp
order by tid asc;


DROP table admin.cttrials2referenceID;
CREATE table admin.cttrials2referenceID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2referenceID
SELECT ct.id, ar.tid
from admin.cttrials2reference ct, admin.ctreference ar
WHERE ct.citation = ar.citation AND ct.PMID = ar.PMID;








update admin.cttrials2results_reference
SET citation = ''
WHERE citation is null;

update admin.cttrials2results_reference
SET PMID = ''
WHERE PMID is null;

DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);
INSERT into admin.ctresults_reference(citation,PMID)
SELECT DISTINCT citation,PMID
from admin.cttrials2results_reference;

INSERT into tmp
SELECT min(tid), citation,PMID
from admin.ctresults_reference
GROUP BY citation,PMID;


DROP table admin.ctresults_reference;
CREATE table admin.ctresults_reference(
	TID 				INTEGER not null generated always as identity primary key,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);
INSERT into admin.ctresults_reference(citation,PMID)
SELECT DISTINCT citation,PMID
from admin.cttrials2results_reference;

DROP table admin.cttrials2results_referenceID;
CREATE table admin.cttrials2results_referenceID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2results_referenceID
SELECT ct.id, ar.tid
from admin.cttrials2results_reference ct, admin.ctresults_reference ar
WHERE ct.citation = ar.citation AND ct.PMID = ar.PMID;

























update admin.cttrials2overall_official
SET first_name = ''
WHERE first_name is null;

update admin.cttrials2overall_official
SET middle_name = ''
WHERE middle_name is null;

update admin.cttrials2overall_official
SET last_name = ''
WHERE last_name is null;

update admin.cttrials2overall_official
SET affiliation = ''
WHERE affiliation is null;

DROP table admin.ctoverall_official;
CREATE table admin.ctoverall_official(
	TID 				INTEGER not null generated always as identity primary key,
	first_name 		VARCHAR(100),
	middle_name 		VARCHAR(100),
	last_name 		VARCHAR(200),
	affiliation 		VARCHAR(300)
);
INSERT into admin.ctoverall_official(first_name,middle_name,last_name,affiliation)
SELECT DISTINCT first_name,middle_name,last_name,affiliation
from admin.cttrials2overall_official;


DROP table admin.cttrials2overall_officialID;
CREATE table admin.cttrials2overall_officialID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2overall_officialID
SELECT ct.id, ar.tid
from admin.cttrials2overall_official ct, CToverall_official ar
WHERE (ct.first_name = ar.first_name) 
	  AND (ct.middle_name = ar.middle_name) 
      AND (ct.last_name = ar.last_name) 
      AND (ct.affiliation = ar.affiliation);






DROP table admin.ctoversight;
CREATE table admin.ctoversight(
	TID 				INTEGER not null generated always as identity primary key,
	oversight_info_authority 	VARCHAR(300)
);
INSERT into admin.ctoversight(oversight_info_authority)
SELECT DISTINCT oversight_info_authority
from admin.cttrials2oversight;

DROP table admin.cttrials2oversightID;
CREATE table admin.cttrials2oversightID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2oversightID
SELECT ct.id, ar.tid
from admin.cttrials2oversight ct, CToversight ar
WHERE ct.oversight_info_authority = ar.oversight_info_authority;







update admin.cttrials2primary_outcomes
SET measure = ''
WHERE measure is null;

update admin.cttrials2primary_outcomes
SET time_frame = ''
WHERE time_frame is null;

update admin.cttrials2primary_outcomes
SET safety_issue = ''
WHERE safety_issue is null;

DROP table admin.ctprimary_outcomes;
CREATE table admin.ctprimary_outcomes(
	TID 				INTEGER not null generated always as identity primary key,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10)
);
INSERT into admin.ctprimary_outcomes(measure,time_frame,safety_issue)
SELECT DISTINCT measure,time_frame,safety_issue
from admin.cttrials2primary_outcomes;

DROP table admin.cttrials2primary_outcomesID;
CREATE table admin.cttrials2primary_outcomesID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2primary_outcomesID
SELECT ct.id, ar.tid
from admin.cttrials2primary_outcomes ct, CTprimary_outcomes ar
WHERE ct.measure = ar.measure AND ct.time_frame = ar.time_frame AND ct.safety_issue = ar.safety_issue;






update admin.cttrials2secondary_outcomes
SET measure = ''
WHERE measure is null;

update admin.cttrials2secondary_outcomes
SET time_frame = ''
WHERE time_frame is null;

update admin.cttrials2secondary_outcomes
SET safety_issue = ''
WHERE safety_issue is null;


DROP table admin.ctsecondary_outcomes;
CREATE table admin.ctsecondary_outcomes(
	TID 				INTEGER not null generated always as identity primary key,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10)
);
INSERT into admin.ctsecondary_outcomes(measure,time_frame,safety_issue)
SELECT DISTINCT measure,time_frame,safety_issue
from admin.cttrials2secondary_outcomes;

DROP table admin.cttrials2secondary_outcomesID;
CREATE table admin.cttrials2secondary_outcomesID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2secondary_outcomesID
SELECT ct.id, ar.tid
from admin.cttrials2secondary_outcomes ct, CTsecondary_outcomes ar
WHERE ct.measure = ar.measure AND ct.time_frame = ar.time_frame AND ct.safety_issue = ar.safety_issue;















