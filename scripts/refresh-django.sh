#!/bin/bash

killall python

/etc/init.d/mysql restart

cd ~/linkedct/ctdjango/cache
./fetchfilelist.sh

cd ~/linkedct/ctdjango/util
python load_urls_from_file.py
python finish-submit-resubmit-refresh-trials.py &

/etc/init.d/apache2 restart



