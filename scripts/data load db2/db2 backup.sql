backup database forxml to c:\backup with 3 buffers buffer 1000 without prompting

db2 "backup database forxml to c:\backup with 3 buffers buffer 1000 without prompting"

from:
http://www.ibm.com/developerworks/data/library/techarticle/pworld/0112mccluney.html

db2 "restore database sample user db2admin using db2admin from c:\backup taken at 20010222145404 with 3 buffers buffer 1000 without rolling forward without prompting"

restore database forxml from c:\db2backup taken at 20100105143849 into oldxml  with 3 buffers buffer 1000 without rolling forward without prompting 