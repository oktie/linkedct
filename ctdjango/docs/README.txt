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


***Coding guideline***

Please follow the industry standard Python PEP8 Coding Style Guide.
http://www.python.org/dev/peps/pep-0008/

A few important items in PEP8:
- Be consistent in naming. ClassName, function_name, variable_name.
- Use long variable names that are indicative.
- NO TABS! Only spaces. 4 spaces for indent.
- A line should be exceed 80 characters!

After you've made changes to files, run the pep8 linter to make sure you've
followed PEP8. To do so, in command line, run:

python pep8 files_to_check
# TODO: Should we get pep8 from somewhere?

I usually just do

python pep8 *.py

This is a relatively large academic project and we have lots of collaborators.
Make sure you think about design before you start coding. While you are coding,
write comments to explain non-obvious things. Minimize repeated code.


***File and Code Structure***

settings.py: all global settings should go here.

pybtex/: pybtex library for parsing bibtex files.
chardet/: library for automatically detecting character encodings.
pagination/: django-pagination plugin.
cache/: where we cache bibtex files.
bibbase/: where bibbase is.
  templates/: all template files.
  temlatetags/: I've created a few bibbase specific template tags here.
  admin.py: controls the admin interface.
  duplication_handler: Jack you should fill this in.
  forms.py: controls the forms used in bibbase.
  models.py: all data models defined here.
  operations.py: I've put the methods that process bibtex files in here.
  urls.py: URL pattern handler.
  views.py: all views.
 

***Data Models and URL Patterns***
Note that all data models inherit from CommonInfo, which contains two fields:
 - name: The name of an object.
 - slug: slug is a URL friendly unique ID for an object.
 
We can access an object using the following URL pattern:
 http://my_server/<object_type>/<slug>/(?format=rdf)
 or
 http://my_server/<object_type>/<object_id>/(?format=rdf)
where object_type is one of: pub, author, journal, series, school, etc.

For example,
 http://my_server/author/fname-lname/              <- this shows you Reynold
 http://my_server/author/1/
 http://my_server/author/fname-lname/?format=rdf   <- redirects to RDF server

To search an object type, 
 http://my_server/search/<object_type>/            <- this shows you the form
 http://my_server/search/<object_type>/<keyword>/  <- this performs the search
 
For authors, I've implemented a special disambiguous hanlding:
 http://my_server/author/<name>/
If <name> matches a slug, return the author. Otherwise, it searches for matches
using four name variations (see views.view_author_disambiguation and
models.Author comment).


***Components to install***

0. Make sure you have Python 2.6 installed. On Windows, make sure Cygwin has Python2.6 (2.5 might be the default)
   We suggest using PyDev plugin for eclipse for development environment.
   On windows, make sure you set the interpreter in PyDev to be the cygwin Python
   e.g., c:\cygwin\bin\python2.6.exe

1. Install easy_install: see instruction at
   http://pypi.python.org/pypi/setuptools
   or just run: sudo apt-get install python-setuptools

2. Use easy_install to install the following components:

sudo easy_install pep8
sudo easy_install django
sudo easy_install pyparsing

easy_install pep8
easy_install django
asy_install pyparsing

3. Install MySQL

a. download source files from MySQL website 
b. install libncurses-devel, ncurses, readline libs in cygwin
 (termcap, libedit libs in cygwin may also be required)
d. MySQL Compile:

tar xzvf mysql-<version>.tar.gz
cd mysql-<version>
./configure -prefix=/usr/local/mysql --without-server --without-readline CFLAGS=-O2
make
make install

4. Run the following command to drop and create mysql database:
echo DROP DATABASE bibbase\; CREATE DATABASE bibbase CHARACTER SET utf8\; | mysql -u root -p -h 127.0.0.1

5. install mysql-python

a) Following the notes on README file of http://sourceforge.net/projects/mysql-python :
tar xfz MySQL-python-1.2.1.tar.gz
cd MySQL-python-1.2.1
# eeit site.cfg if necessary (for MySQL)
# You may have to modify site.cfg and uncomment/change it to have this line:
# mysql_config = /usr/local/mysql/bin/mysql_config
python setup.py build
sudo python setup.py install # or su first

6. modify the DATABASES variable in settings.py file to point to your database/user/password combination 


7. To run this

python manage.py syncdb
python manage.py runserver


8. Run the following command to import buzzwords (you may need to put these files into the folder with models.py)
cd util/linkage
./import_buzzwords.sh

9. Run the following command to import DBLP authors
cd util/linkage
./import_dblp_authors.sh


***Automatic Backup***
Please refer to the README.txt in utils/



