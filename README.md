# Introduction

This repo is a fork and shortend version from [original roster](https://github.com/ielizaga/roster), this web app helps to manage team availability, below is a screenshot of how the web app looks.

#### Main page

![main page](https://github.com/faisaltheparttimecoder/EMEARoster/blob/master/Core/static/Core/img/main_screen.png)

#### Edit panel

![Edit panel](https://github.com/faisaltheparttimecoder/EMEARoster/blob/master/Core/static/Core/img/edit_availability.png)

... etc

# Requirements

+ Python 2.7
+ Django 1.10

# Setup

+ In Order to use this repo, clone the repo

```
git clone https://github.com/faisaltheparttimecoder/EMEARoster.git
```

+ Install all the requirements

```
pip install -r requirements.txt
```

+ Create a run file ( eg run_dev.sh ) and update the below secret of your environment

```
#!/usr/bin/env bash
set +H
export DB_ENGINE='django.db.backends.mysql'                              # If you are using mysql to store the information else read different engines here https://docs.djangoproject.com/en/1.10/ref/settings/#databases
export DB_NAME='DB_NAME'                                                 # Database name                     
export DB_USER='DB_USER'                                                 # Database user
export DB_PASS='DB_PASS'                                                 # Database user password
export DB_HOST='DB_HOST'                                                 # Database Host
export DB_PORT='DB_PORT'                                                 # Database Port
export ADMIN_PASS='ADMIN_PASS'                                           # Provide the password that need to be used by the app to create the superuser in the database ( i.e for django admin page ) , if admin already created the app skips the step
export SECRET_KEY="SECRET_KEY"                                           # SECRET KEY of the Django app, i.e that key obtain when you run "Python Manage.py startproject" on Django
export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY="OUTH_KEY"                          # Google Authentication key to authenticate the user using google authentication ( https://console.developers.google.com )
export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="OUTH_SECRET"                    # Google Authentication Secret
export SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS="Email domain"      # Domain name who email will be whitelisted others would be error'ed out ( i.e gmail.com etc )
export SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE1="profile"                        # We just need profile information of users.
python manage.py runserver --insecure
```

+ Once the above information is correctly entered you can run the file to start using the app.

```
/bin/sh run_dev.sh
```

+ Now open up a browser and using the below URL to access the app

```
http://127.0.0.1:8000/
```
