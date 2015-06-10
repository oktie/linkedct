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

# Django settings for ctdjango project.

import os

DEBUG = True#False 
TEMPLATE_DEBUG = DEBUG
APP_ROOT_DIR = os.path.dirname(__file__)

PAGINATION_INVALID_PAGE_RAISES_404 = True


HOME_CONFIG = {
    'HOME': 'http://server.name/linkedct',
    'ROOT': '/linkedct/resource/',
    'RDF_ROOT': '/data/',
    'MEDIAROOT': '/home/user/workspace/linkedct/trunk/ctdjango/linkedct/static/',
    'XML_SIZE_LIMIT': 500 * 1024,  # in KB
    'D2R_SERVER': 'http://localhost:2020/',
    'D2RMAP': '@prefix map:     <file:/home/user/workspace/linkedct/d2r-server/d2r-server-0.7/initial-linkedct-live.n3#> .\n',
    'RECOVER_LOC': os.path.join(APP_ROOT_DIR, 'cache/list.txt'),
    'SOURCES_FILE_LOC': os.path.join(APP_ROOT_DIR, 'cache/'),
    'AWS_ACCESS_KEY': '',
    'AWS_SECRET_KEY': '',
    'BUCKET_NAME': '25048f14379dfe2191d7f606ee62fb2c',
    'URL_BACKUP_KEY': 'URL_BAK',
}

SERVER_CONFIG = {
    'HOME': 'http://data.linkedct.org',
    'ROOT': '/resource/',
    'RDF_ROOT': '/data/',
    'MEDIAROOT': '/root/linkedct/media',
    #'ROOT': '/resource/',
    'XML_SIZE_LIMIT': 500 * 1024,  # in KB
    'D2R_SERVER': 'http://localhost:2020/',
    'D2RMAP': '@prefix map:     <file:/root/linkedct/d2r-server/d2r-server-0.7/initial-linkedct-live.n3#> .\n',
    'RECOVER_LOC': os.path.join(APP_ROOT_DIR, 'cache/list.txt'),
    'SOURCES_FILE_LOC': os.path.join(APP_ROOT_DIR, 'cache/'),
    'AWS_ACCESS_KEY': '',
    'AWS_SECRET_KEY': '',
    'BUCKET_NAME': '25048f14379dfe2191d7f606ee62fb2c',
    'URL_BACKUP_KEY': 'URL_BAK',
}

CS_CONFIG = {
#    'HOME': 'http://www.cs.toronto.edu:40104',
    'HOME': 'http://data.linkedct.org',
    'ROOT': '/resource/',
    'RDF_ROOT': '/data/',
    'MEDIAROOT': '/root/linkedct/media',
    #'ROOT': '/resource/',
    'XML_SIZE_LIMIT': 500 * 1024,  # in KB
    'D2R_SERVER': 'http://localhost:40116/',
    'D2RMAP': '    xmlns:map="file:/home/user/workspace/linkedct/d2r-server/d2r-server-0.7/initial-linkedct-live.n3#"\n',
    'RECOVER_LOC': os.path.join(APP_ROOT_DIR, 'cache/list.txt'),
    'SOURCES_FILE_LOC': os.path.join(APP_ROOT_DIR, 'cache/'),
    'AWS_ACCESS_KEY': '',
    'AWS_SECRET_KEY': '',
    'BUCKET_NAME': '25048f14379dfe2191d7f606ee62fb2c',
    'URL_BACKUP_KEY': 'URL_BAK',
}


CONFIG = CS_CONFIG

ADMINS = (
    ('Oktie Hassanzadeh', 'oktie@spam.oktie.com'),
)

MANAGERS = ADMINS

SQLITE_SETTINGS = {
    'ENGINE': 'sqlite3',
    'NAME': os.path.join(APP_ROOT_DIR, 'sqlite3.db'),
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
}

MYSQL_SETTINGS = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'hostname',
        'PORT': 'portnumber',
        'init_command': 'SET storage_engine=INNODB',
        #'HOST': '/u/user/site/conf/run/mysqld.sock',
}

POSTGRES_SETTINGS = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',                      
        'USER': 'user',
        'PASSWORD': 'password',                
}


DATABASES = {
    'default': MYSQL_SETTINGS,
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
MEDIA_ROOT = CONFIG['MEDIAROOT']

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: 'http://foo.com/media/', '/media/'.
ADMIN_MEDIA_PREFIX = '/static/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's=tc%)i4u-kn8-tz0=()t(y+5$*b+1&w148p(ybx8o3#m7mfc4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like '/home/html/django_templates' or
    # 'C:/www/django/templates'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'home/masayo/workspace/CTDjango/trunk/ctdjango/templates'
)

CACHE_MIDDLEWARE_SECONDS = 100000 
CACHE_MIDDLEWARE_KEY_PREFIX = 'ctdjango'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'file:///u/user/tmp/django_cache'

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'pagination',
    'linkedct',
    'databrowse',
)
