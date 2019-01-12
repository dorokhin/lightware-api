## LightWare RESTFUL API
[![codecov](https://codecov.io/gh/dorokhin/lightware-api/branch/master/graph/badge.svg)](https://codecov.io/gh/dorokhin/lightware-api)

### Console commands

    To run test: make tests

    To run application: make run

    To run all commands at once : make all


### App URL

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"
    

### Coverage & tests

`coverage run --source app  manage.py test`

`coverage report`

