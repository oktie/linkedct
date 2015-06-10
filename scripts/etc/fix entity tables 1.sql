delete from ctintervention;

select * from ctintervention;
insert into ctintervention values(DEFAULT,'sd','sd','sd');


select * from ctintervention;

alter table ctintervention alter column tid SET DATA TYPE INTEGER;
alter table ctintervention alter column tid SET not null;
alter table ctintervention alter column tid DROP identity;
alter table ctintervention alter column tid SET generated always as identity;

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


insert into ctintervention(intervention_type, intervention_name, description) select intervention_type, intervention_name, description from TMP order by tid desc;







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

insert into ctintervention(intervention_type, intervention_name, description) select intervention_type, intervention_name, description from TMP order by tid desc;




