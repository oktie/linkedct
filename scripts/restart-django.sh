#!/bin/bash

killall python

/etc/init.d/mysql restart

/etc/init.d/apache2 restart

cd ~/linkedct/ctdjango/util
python finish-submit-resubmit-refresh-trials.py &


