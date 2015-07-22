# LinkedCT

[Project description goes in here]

## Development Guide

### Install dependencies

Use pip to install dependencies:

```
pip install -r requirements.txt
```

Note for "EnvironmentError: mysql\_config not found" error: 
if you are on Ubuntu,
install the package `libmysqlclient-dev`.

### Set up MySQL database

To set up a MySQL database for the Django site on your machine,
first install MySQL and then create a database called `ctdjango`.
You may want to create a new user with full privilege on `ctdjango`.

Create a new file named `mysql.json` in the same directory as this README 
file.
In the file, copy and paste the JSON template below and fill in the
corresponding information.

```json
{
	"NAME" : "ctdjango",
	"USER" : "<user name of the database user for ctdjango>",
	"PASSWORD" : "<the password for that user>",
	"HOST" : "<your mysql database server, typically just 'localhost'>"
} 
```

Now use Django to create tables in the database before we can use them:

```
python manage.py migrate
```
