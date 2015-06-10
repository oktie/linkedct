DROP table ctintervention;
CREATE table ctintervention(
	TID 				INTEGER not null generated always as identity primary key,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 		VARCHAR(2000)
);

DROP table tmp;
CREATE table tmp(
	TID 				INTEGER not null primary key,
	intervention_type 	VARCHAR(100),
	intervention_name 	VARCHAR(200),
	description 		VARCHAR(2000)
);

import from "C:\Users\admin\dcp-workspace\linkeddata\linkedct\data\mysql\ctintervention.csv" 
OF DEL MODIFIED BY DELPRIORITYCHAR CHARDEL"" COLDEL, MESSAGES "c:\Users\admin\tmp.txt" 
INSERT INTO tmp;

insert into ctintervention(intervention_type, intervention_name, description) 
select intervention_type, intervention_name, description from TMP 
order by tid asc;

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
	  






DROP table admin.ctcondition;
CREATE table admin.ctcondition(
	TID 				INTEGER not null generated always as identity primary key,
	condition 	VARCHAR(200)
);

DROP table tmp2;
CREATE table tmp2(
	TID 				INTEGER not null primary key,
	condition 	VARCHAR(200)
);


import from "C:\Users\admin\dcp-workspace\linkeddata\linkedct\data\mysql\ctcondition.csv" 
OF DEL MODIFIED BY DELPRIORITYCHAR CHARDEL"" COLDEL, MESSAGES "c:\Users\admin\tmp.txt" 
INSERT INTO tmp2;

INSERT into admin.ctcondition(condition)
select condition from TMP2 
order by tid asc;

INSERT into admin.ctcondition(condition)
SELECT DISTINCT condition
from admin.cttrials2condition
WHERE condition!='' AND condition NOT IN (SELECT condition FROM tmp2);

DROP table admin.cttrials2conditionID;
CREATE table admin.cttrials2conditionID(
    ID 			CHAR(11),
    TID 		INTEGER
);

INSERT into admin.cttrials2conditionID
SELECT ct.id, co.tid
from admin.cttrials2condition ct, CTcondition co
WHERE ct.condition=co.condition;













DROP table admin.ctlocation;
CREATE table admin.ctlocation(
	TID 				INTEGER not null generated always as identity primary key,
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200), 
	facility_address_state 		VARCHAR(200), 
	facility_address_zip 		VARCHAR(200),
	facility_address_country 	VARCHAR(200)
);

DROP table tmp3;
CREATE table tmp3(
	TID 				INTEGER not null primary key,
	facility_name 			VARCHAR(400),
	facility_address_city 		VARCHAR(200), 
	facility_address_state 		VARCHAR(200), 
	facility_address_zip 		VARCHAR(200),
	facility_address_country 	VARCHAR(200)
);

import from "C:\Users\admin\dcp-workspace\linkeddata\linkedct\data\mysql\ctlocation.csv" 
OF DEL MODIFIED BY DELPRIORITYCHAR CHARDEL"" COLDEL, MESSAGES "c:\Users\admin\tmp.txt" 
INSERT INTO tmp3;

INSERT into admin.ctlocation(facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country) 
select facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country from TMP3
order by tid asc;

INSERT into admin.ctlocation(facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country)
SELECT DISTINCT facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country
from admin.cttrials2location
WHERE (facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country) NOT IN
(SELECT facility_name,facility_address_city, facility_address_state, facility_address_zip, facility_address_country FROM TMP3);

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














