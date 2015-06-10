#IMPORT FROM C:/ctdata/trials.del OF DEL XML FROM C:/ctdata/data INSERT INTO tst

DROP TABLE ctxmlnew;

CREATE TABLE ctxmlnew (
id char(11),
trial xml
);

IMPORT FROM C:/ctdata/trials.del OF DEL XML FROM C:/ctdata/data COMMITCOUNT 1000
INSERT INTO ctxmlnew
