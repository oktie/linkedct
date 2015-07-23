# LinkedCT

[Project description goes in here]

## Development guide

### Install dependencies

Use pip to install dependencies:

```
pip install -r requirements.txt
```

Note for "EnvironmentError: mysql\_config not found" error: 
if you are on Ubuntu,
install the package `libmysqlclient-dev`.

### Set up Django web app

First create a configuration file named `config.json`. 
An example is given as `config.json.sample`.
Just do `cp config.json.sample config.json`, and fill out the `DATABASE`
settings according to your database. The default settings for database
is using SQLite, which is probably the simplest for development.

Now use Django to create tables in the database before we can use them:

```
python manage.py migrate
```

To start the development server:

```
python manage.py runserver
```
