## LightWare RESTFUL API
[![codecov](https://codecov.io/gh/dorokhin/lightware-api/branch/master/graph/badge.svg)](https://codecov.io/gh/dorokhin/lightware-api)
[![Build Status](https://travis-ci.org/dorokhin/lightware-api.svg?branch=master)](https://travis-ci.org/dorokhin/lightware-api)
[![Requirements Status](https://requires.io/github/dorokhin/lightware-api/requirements.svg?branch=master)](https://requires.io/github/dorokhin/lightware-api/requirements/?branch=master)
![](https://img.shields.io/github/license/dorokhin/lightware-api.svg?logoColor=brightgreen&style=social)
[![Maintainability](https://api.codeclimate.com/v1/badges/cb1ea70bb4d46276a2aa/maintainability)](https://codeclimate.com/github/dorokhin/lightware-api/maintainability)

### Console commands

    To run test: make tests

    To run application: make run

    To run all commands at once : make all

### Migration

    `python manage.py db init` create migration
    `python manage.py db migrate` migrate db
    `python manage.py db upgrade` upgrade db to current revision
    `python manage.py db --help` print help

### App URL

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman

    Authorization header is in the following format:

    Key: Authorization
    Value: "Bearer token_generated_during_login"
    

### Coverage & tests

`coverage run --source app  manage.py test`

`coverage report`

