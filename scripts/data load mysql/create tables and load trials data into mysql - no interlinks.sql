DROP TABLE IF EXISTS CTtrials;
CREATE TABLE CTtrials (
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
	`phase` 			VARCHAR(100),
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
	overall_contact_email 			VARCHAR(100),
	start_date 			VARCHAR(100),
	end_date  			VARCHAR(100),
	primary_completion_date 	VARCHAR(100),
	verification_date 		VARCHAR(100),
	lastchanged_date 		VARCHAR(100),
	firstreceived_date 		VARCHAR(100),
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS CTtrials2secid;
CREATE TABLE CTtrials2secid(
	ID char(11) NOT NULL,
	secondary_id 	VARCHAR(100)
);

DROP TABLE IF EXISTS CTtrials2nctalias;
CREATE TABLE CTtrials2nctalias(
	ID char(11) NOT NULL,
	nct_alias 	VARCHAR(100)
);
     
DROP TABLE IF EXISTS CTtrials2collabagency;
CREATE TABLE CTtrials2collabagency(
	ID char(11) NOT NULL,
	collaborator_agency 	VARCHAR(300)
);

DROP TABLE IF EXISTS CTtrials2oversight;
CREATE TABLE CTtrials2oversight(
	ID char(11) NOT NULL,
	oversight_info_authority 	VARCHAR(300)
);


DROP TABLE IF EXISTS CTtrials2condition;
CREATE TABLE CTtrials2condition(
	ID char(11) NOT NULL,
	`condition` 	VARCHAR(200)
);


DROP TABLE IF EXISTS CTtrials2primary_outcomes;
CREATE TABLE CTtrials2primary_outcomes(
	ID char(11) NOT NULL,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10) 
);


DROP TABLE IF EXISTS CTtrials2secondary_outcomes;
CREATE TABLE CTtrials2secondary_outcomes(
	ID char(11) NOT NULL,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10) 
);


DROP TABLE IF EXISTS CTtrials2arm_group;
CREATE TABLE CTtrials2arm_group(
	ID char(11) NOT NULL,
	arm_group_label 	VARCHAR(100),
	arm_group_type  	VARCHAR(100),
	description		VARCHAR(2000)
);

DROP TABLE IF EXISTS CTtrials2intervention;
CREATE TABLE CTtrials2intervention(
	ID char(11) NOT NULL,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 	VARCHAR(2000)
);


DROP TABLE IF EXISTS CTintervention2arm;
CREATE TABLE CTintervention2arm(
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 	VARCHAR(2000),
	arm_group_label VARCHAR(100)
);


DROP TABLE IF EXISTS CTintervention2other_name;
CREATE TABLE CTintervention2other_name(
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 	VARCHAR(2000),
	other_name 	VARCHAR(200) 
);



DROP TABLE IF EXISTS CTtrials2overall_official;
CREATE TABLE CTtrials2overall_official(
	ID char(11) NOT NULL,
	first_name 		VARCHAR(100),
	middle_name 		VARCHAR(100),
	last_name 		VARCHAR(200),
	degrees 		VARCHAR(100),
	role 			VARCHAR(200),
	affiliation 		VARCHAR(300)
);


DROP TABLE IF EXISTS CTtrials2location;
CREATE TABLE CTtrials2location(
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



DROP TABLE IF EXISTS CTlocation2investigator;
CREATE TABLE CTlocation2investigator(
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




DROP TABLE IF EXISTS CTtrials2reference;
CREATE TABLE CTtrials2reference(
	ID char(11) NOT NULL,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);



DROP TABLE IF EXISTS CTtrials2results_reference;
CREATE TABLE CTtrials2results_reference(
	ID char(11) NOT NULL,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100)
);



DROP TABLE IF EXISTS CTtrials2link;
CREATE TABLE CTtrials2link(
	ID char(11) NOT NULL,
	url 				VARCHAR(400), 
	description 			VARCHAR(2000)
);

















DROP TABLE IF EXISTS CTtrials_summary;
CREATE TABLE CTtrials_summary (
	id	CHAR(11) NOT NULL,
	brief_summary 		text,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS CTtrials_description;
CREATE TABLE CTtrials_description (
	id	CHAR(11) NOT NULL,
	detailed_description 	text,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS CTtrials_biospec;
CREATE TABLE CTtrials_biospec (
	id	CHAR(11) NOT NULL,
	biospec_descr 		text,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS CTtrials_criteria;
CREATE TABLE CTtrials_criteria (
	id	CHAR(11) NOT NULL,
	eligibility_criteria		text,
	PRIMARY KEY(id)
);









DROP TABLE IF EXISTS CTintervention;
CREATE TABLE CTintervention(
	TID 				INTEGER,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 		VARCHAR(2000),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2interventionID;
CREATE TABLE CTtrials2interventionID(
    ID 			CHAR(11),
	TID 		INTEGER,
	FOREIGN KEY(ID) REFERENCES CTtrials(id),
	FOREIGN KEY(TID) REFERENCES CTintervention(tid)
);





DROP TABLE IF EXISTS CTcondition;
CREATE TABLE CTcondition(
	TID 				INTEGER,
	`condition` 	VARCHAR(200),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2conditionID;
CREATE TABLE CTtrials2conditionID(
    ID 			CHAR(11),
    TID 		INTEGER
);






DROP TABLE IF EXISTS CTarm_group;
CREATE TABLE CTarm_group(
	TID 				INTEGER,
	arm_group_label 	VARCHAR(100),
	arm_group_type  	VARCHAR(100),
	description		VARCHAR(2000),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2arm_groupID;
CREATE TABLE CTtrials2arm_groupID(
    ID 			CHAR(11),
    TID 		INTEGER
);





DROP TABLE IF EXISTS CTcollabagency;
CREATE TABLE CTcollabagency(
	TID 				INTEGER,
	collaborator_agency 	VARCHAR(300),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2collabagencyID;
CREATE TABLE CTtrials2collabagencyID(
    ID 			CHAR(11),
    TID 		INTEGER
);







DROP TABLE IF EXISTS CTlink;
CREATE TABLE CTlink(
	TID 				INTEGER,
	url 				VARCHAR(400), 
	description 			VARCHAR(2000),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2linkID;
CREATE TABLE CTtrials2linkID(
    ID 			CHAR(11),
    TID			INTEGER

);




DROP TABLE IF EXISTS CTlocation;
CREATE TABLE CTlocation(
	TID 				INTEGER,
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200), 
	facility_address_state 		VARCHAR(200), 
	facility_address_zip 		VARCHAR(200),
	facility_address_country 	VARCHAR(200),
	PRIMARY KEY(TID)
);


DROP TABLE IF EXISTS CTtrials2locationID;
CREATE TABLE CTtrials2locationID(
    ID 			CHAR(11),
    TID 		INTEGER
);





DROP TABLE IF EXISTS CToverall_official;
CREATE TABLE CToverall_official(
	TID 				INTEGER,
	first_name 		VARCHAR(100),
	middle_name 		VARCHAR(100),
	last_name 		VARCHAR(200),
	affiliation 		VARCHAR(300),
	PRIMARY KEY(TID)
);


DROP TABLE IF EXISTS CTtrials2overall_officialID;
CREATE TABLE CTtrials2overall_officialID(
    ID 			CHAR(11),
    TID 		INTEGER
);




DROP TABLE IF EXISTS CToversight;
CREATE TABLE CToversight(
	TID 				INTEGER,
	oversight_info_authority 	VARCHAR(300),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2oversightID;
CREATE TABLE CTtrials2oversightID(
    ID 			CHAR(11),
    TID 		INTEGER
);





DROP TABLE IF EXISTS CTprimary_outcomes;
CREATE TABLE CTprimary_outcomes(
	TID 				INTEGER,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2primary_outcomesID;
CREATE TABLE CTtrials2primary_outcomesID(
    ID 			CHAR(11),
    TID 		INTEGER
);




DROP TABLE IF EXISTS CTsecondary_outcomes;
CREATE TABLE CTsecondary_outcomes(
	TID 				INTEGER,
	measure 	VARCHAR(400),
	time_frame 	VARCHAR(300),
	safety_issue 	VARCHAR(10),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2secondary_outcomesID;
CREATE TABLE CTtrials2secondary_outcomesID(
    ID 			CHAR(11),
    TID 		INTEGER
);



DROP TABLE IF EXISTS CTreference;
CREATE TABLE CTreference(
	TID 				INTEGER,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2referenceID;
CREATE TABLE CTtrials2referenceID(
    ID 			CHAR(11),
    TID 		INTEGER
);

DROP TABLE IF EXISTS CTresults_reference;
CREATE TABLE CTresults_reference(
	TID 				INTEGER,
	citation 			VARCHAR(10000),
	PMID 				VARCHAR(100),
	PRIMARY KEY(TID)
);

DROP TABLE IF EXISTS CTtrials2results_referenceID;
CREATE TABLE CTtrials2results_referenceID(
    ID 			CHAR(11),
    TID 		INTEGER
);


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials.txt'
INTO TABLE CTtrials
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2secid.txt'
INTO TABLE CTtrials2secid
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2nctalias.txt'
INTO TABLE CTtrials2nctalias
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2collabagency.txt'
INTO TABLE CTtrials2collabagency
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2oversight.txt'
INTO TABLE CTtrials2oversight
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2condition.txt'
INTO TABLE CTtrials2condition
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2primary_outcomes.txt'
INTO TABLE CTtrials2primary_outcomes
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2secondary_outcomes.txt'
INTO TABLE CTtrials2secondary_outcomes
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2arm_group.txt'
INTO TABLE CTtrials2arm_group
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2intervention.txt'
INTO TABLE CTtrials2intervention
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTintervention2arm.txt'
INTO TABLE CTintervention2arm
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTintervention2other_name.txt'
INTO TABLE CTintervention2other_name
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2overall_official.txt'
INTO TABLE CTtrials2overall_official
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2location.txt'
INTO TABLE CTtrials2location
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTlocation2investigator.txt'
INTO TABLE CTlocation2investigator
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2reference.txt'
INTO TABLE CTtrials2reference
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2results_reference.txt'
INTO TABLE CTtrials2results_reference
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2link.txt'
INTO TABLE CTtrials2link
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials_summary.txt'
INTO TABLE CTtrials_summary
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials_description.txt'
INTO TABLE CTtrials_description
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials_biospec.txt'
INTO TABLE CTtrials_biospec
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials_criteria.txt'
INTO TABLE CTtrials_criteria
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';





LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTintervention.txt'
INTO TABLE CTintervention
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2interventionID.txt'
INTO TABLE CTtrials2interventionID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';



LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTcondition.txt'
INTO TABLE CTcondition
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2conditionID.txt'
INTO TABLE CTtrials2conditionID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTarm_group.txt'
INTO TABLE CTarm_group
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2arm_groupID.txt'
INTO TABLE CTtrials2arm_groupID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTcollabagency.txt'
INTO TABLE CTcollabagency
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2collabagencyID.txt'
INTO TABLE CTtrials2collabagencyID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTlink.txt'
INTO TABLE CTlink
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2linkID.txt'
INTO TABLE CTtrials2linkID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTlocation.txt'
INTO TABLE CTlocation
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2locationID.txt'
INTO TABLE CTtrials2locationID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CToverall_official.txt'
INTO TABLE CToverall_official
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2overall_officialID.txt'
INTO TABLE CTtrials2overall_officialID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CToversight.txt'
INTO TABLE CToversight
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2oversightID.txt'
INTO TABLE CTtrials2oversightID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTprimary_outcomes.txt'
INTO TABLE CTprimary_outcomes
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2primary_outcomesID.txt'
INTO TABLE CTtrials2primary_outcomesID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTsecondary_outcomes.txt'
INTO TABLE CTsecondary_outcomes
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2secondary_outcomesID.txt'
INTO TABLE CTtrials2secondary_outcomesID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTreference.txt'
INTO TABLE CTreference
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2referenceID.txt'
INTO TABLE CTtrials2referenceID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTresults_reference.txt'
INTO TABLE CTresults_reference
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE 'C:/data/ctdump/CTtrials2results_referenceID.txt'
INTO TABLE CTtrials2results_referenceID
FIELDS OPTIONALLY ENCLOSED BY '"' TERMINATED BY ','
LINES TERMINATED BY '\r\n';







