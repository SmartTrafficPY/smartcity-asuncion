# SmartTraffic-SmartCityAsuncion
La plataforma del servidor del proyecto SmartTraffic

## REQUIREMENTS

### docker & docker-compose
Docker: 18.03 + (see https://docs.docker.com/install/)
Docker Compose: 1.13.0 + (see https://docs.docker.com/compose/install/)

### WSL
Using WSL? Get it to play nicely with docker. See https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly.
Using Docker Toolbox? You might need to look here:
https://gist.github.com/strarsis/44ded0d254066d9cb125ebbb04650d6c to set it up.

### Optional: Postgresql
The psql utility will come in handy if you need to inspect the database. Install it on your environment:

```
sudo apt-get install -y postgresql-client-10
```

### Python environment
Install `pyenv` (maybe through [anyenv](https://github.com/anyenv/anyenv)) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for a flexible python development environment.

## Installation
Clone the repository:
```
git clone https://github.com/SmartTrafficPY/smartcity-asuncion.git
```

### Python version and the virtual environment
Install and select the python version specified in `.python-version` (v3.7.2)

```
pyenv install 3.7.2
pyenv local 3.7.2
pip install -U pip
```

Install pipenv:
```
pip install pipenv
```

Let pipenv create a virtual environment and install all the required dependencies:
```
pipenv install --dev
```

Activate your virtual environment: 

```
pipenv shell
```

### Keeping a congruent code style
Install pre-commit hooks to lint and uniformise code style:
```
pre-commit install
```

### First time tasks
Fire up the companion services:
```
docker-compose up
```
It'll take some time for postgres to create the admin database and start listening on port 5432.

Create the database:
```
python manage.py createdb
```

Create the table needed for caching:
```
python manage.py createcachetable
```

Create all the other tables:
```
python manage.py migrate
```

Populate your tables with development fixtures:
```
python manage.py loaddata initial
```

Create an admin user:
```
python manage.py createsuperuser
```

### Running the service
With the virtual environment active, you can start the service:
```
python manage.py runserver 8000
```
If your browser runs on another node, you may need to do a `python manage.py runserver 0.0.0.0:8000` instead, so it binds to all interfaces.

## Deployment

Building a new image:
```
$ scripts/build-docker <TAG>
```
Use YYYYMMDD or YYYYMMDD.HHMM to tag production releases. Omit `<TAG>` for staging builds (it will default to `test`). 

Restart the service:
```
$ docker-compose down
$ docker-compose up 
```

deploy
define postgres.env and smartcity.env

docker-compose run smartcity python manage.py createdb
docker-compose run smartcity python manage.py migrate
docker-compose run smartcity python manage.py loaddata initial
docker-compose run smartcity python manage.py createsuperuser


docker-compose run smartcity python manage.py migrate
docker-compose run smartcity /build-staticfiles.sh

loading spots
cat spots.geojson | docker-compose run smartcity python manage.py loadspots 1

You'll find the app is running on http://127.0.0.1:8000
or in the docker VM if you are running in docker toolbox, that you may known with the following command

```
$ docker-machine ip
$ 132.145.199.13
```

## SmartParking: understanding server requests
This rant assumes the service is available at 127.0.0.1, port 8000.

### User Management
The platform works with:
- session-based authentication
- token-based authentication (the DRF simple ones)

All requests must be authenticated. Superusers and staff can perform all requests.

Your app needs to use credentials that represent the app itself (as opposed to a normal user account) to perform:

#### List users:
GET /smartparking/users/
```
$ curl -H "Authorization: Token aTokenForTheSmartParkingApp" -iX GET http://127.0.0.1:8000/smartparking/users/
```
(you'll get a long JSON array)


#### Create a user:
POST /smartparking/users/
```
$ curl -d '{"username": "normal_user", "password": "superSecretPassword", "smartparkingprofile": {"birth_date": "2009-01-01", "sex": "M"}}' -H "Content-Type: application/json" -H "Authorization: Token aTokenForTheSmartParkingApp" -iX POST http://127.0.0.1:8000/smartparking/users/

HTTP/1.1 201 Created
Date: Sun, 01 Sep 2019 17:13:01 GMT
Server: WSGIServer/0.2 CPython/3.7.2
Content-Type: application/json
Location: http://127.0.0.1:8000/smartparking/users/1234/
Vary: Accept, Cookie
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 181

{"url":"http://127.0.0.1:8000/smartparking/users/1234/","username":"normal_user","smartparkingprofile":{"birth_date":"2009-01-01","sex":"M"}}
```

Get the URL in the `Location:` header to manipulate the user instance you just created.

#### Retrieve a user's token:
```
curl -d '{"username": "normal_user", "password": "superSecretPassword"}' -H "Content-Type: application/json" -H "Authorization: Token aTokenForTheSmartParkingApp" -X POST http://127.0.0.1:8000/smartparking/auth-token/

{"token":"normalUserToken", "url":"http://127.0.0.1:8000/smartparking/users/1234/"}
```


If you want to modify user details, you need to authenticate as that user (or as a superuser or staff).

#### Change user information:
PATCH /smartparking/users/_someUserId_
```
$ curl -d '{"password": "aBetterSuperSecretPassword"}' -H "Content-Type: application/json" -H "Authorization: Token normalUserToken" -iX PATCH http://127.0.0.1:8000/smartparking/users/1234/

HTTP/1.1 200 OK
Date: Sun, 01 Sep 2019 18:10:03 GMT
Server: WSGIServer/0.2 CPython/3.7.2
Content-Type: application/json
Vary: Accept, Cookie
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 139

{"url":"http://127.0.0.1:8000/smartparking/users/1234/","username":"normal_user","smartparkingprofile":{"birth_date":"2009-01-01","sex":"M"}}
```

## Some notes regarding docker on windows 
If you are getting this error, `docker : /bin/sh^M: bad interpreter: No such file or directory`
You would like to see this page to solve it: https://forums.docker.com/t/error-while-running-docker-code-in-powershell/34059

Other thing that might be useful is restarting docker, that may solve some troubles of network.

```
$ docker-machine restart
```
