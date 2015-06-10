#!/bin/bash
exec >/dev/null

/usr/local/tomcat/bin/shutdown.sh
killall java

cd ~/linkedct/d2r-server/d2r-server-0.7/
cp log4.txt log5.txt
cp log3.txt log4.txt
cp log2.txt log3.txt
cp log1.txt log2.txt

./d2r-server linkedct-live.n3 --fast > log1.txt &

/usr/local/tomcat/bin/startup.sh

