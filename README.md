# SmartTraffic-SmartCityAsuncion
La plataforma del servidor del proyecto SmartTraffic

## REQUIREMENTS

You need to install this to have fun with our project.

### docker & docker-compose
Docker: 18.03 +
Docker Compose: 1.13.0 +
Check that you have the correct docker version, with docker compose too,
if you have linux OS, you have to do it separately:

```
$ docker --version
Docker version 18.03.0-ce, build 0429c243o2
$ docker-compose --version
docker-compose version 1.20.1, build 0429c243o2
```

If not installed yet, follow the official guide in https://docs.docker.com/install/ and docker-compose here: https://docs.docker.com/compose/install/

### Windows Users only

If you are a Linux users, you are good to go, if you are a windows user, im sorry mate, but you need to follow 
the next steps and guides for preparing the deployment.

Set docker for using WSL, following the next guide:
https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly

If you are using Docker Toolbox, because of your Windows build version, you might need to look 
https://gist.github.com/strarsis/44ded0d254066d9cb125ebbb04650d6c for set docker right.

We have already set docker in our WSL, so next we need to make our dev environment properly for our platform.
Windows users for now on, you will work in your new Ubuntu WSL console.

### Python

You need to have install python, check it by using:

```
$ python -V
```
If you have not python, follow the next [guide](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/)

### Postgresql

Make sure you have postgres 10 with:

```
$ sudo apt-get install -y postgresql-client-10
$ psql --version  
```

### Anyenv

Install this tool, [anyenv](https://github.com/anyenv/anyenv) to have a really develop environment.
Make sure that even you close your current console, anyenv persist.

### Python environment

Now the Linux users can join us, use your WSL if you are Windows user, we need to prepare a develop environment for 
the server to execute.

First install some packages pyenv will need to build, compile the commands we need to run after, so:

```
sudo apt-get update; sudo apt-get install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
Clone the repository:
```
git clone https://github.com/SmartTrafficPY/smartcity-asuncion.git
```
Go to directory of the repository and then, we can install python version 3.7.2 and pip with:
```
cd .../smartcity-asuncion
```
```
$ pyenv install 3.7.2
$pip install -U pip
$pip install pipenv
$pipenv install --dev
```
if you had a problem with psycopg2 while executing `pipenv install --dev` having this similar output error:

```
Installing dependencies from Pipfile.lock (0159e3)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 27/27 — 00:00:04
An error occurred while installing psycopg2==2.8.3 --hash=sha256:128d0fa910ada0157bba1cb74a9c5f92bb8a1dca77cf91a31eb274d1f889e001 --hash=sha256:227fd46cf9b7255f07687e5bde454d7d67ae39ca77e170097cdef8ebfc30c323 --hash=sha256:2315e7f104681d498ccf6fd70b0dba5bce65d60ac92171492bfe228e21dcc242 --hash=sha256:4b5417dcd2999db0f5a891d54717cfaee33acc64f4772c4bc574d4ff95ed9d80 --hash=sha256:640113ddc943522aaf71294e3f2d24013b0edd659b7820621492c9ebd3a2fb0b --hash=sha256:897a6e838319b4bf648a574afb6cabcb17d0488f8c7195100d48d872419f4457 --hash=sha256:8dceca81409898c870e011c71179454962dec152a1a6b86a347f4be74b16d864 --hash=sha256:b1b8e41da09a0c3ef0b3d4bb72da0dde2abebe583c1e8462973233fd5ad0235f --hash=sha256:cb407fccc12fc29dc331f2b934913405fa49b9b75af4f3a72d0f50f57ad2ca23 --hash=sha256:d3a27550a8185e53b244ad7e79e307594b92fede8617d80200a8cce1fba2c60f --hash=sha256:f0e6b697a975d9d3ccd04135316c947dd82d841067c7800ccf622a8717e98df1! Will try again.
```
You must uninstall psycopg2 and then install psycopg2-binary
```
pipenv uninstall psycopg2
pipenv install  psycopg2-binary
```
And then try again `pipenv install --dev`

Then we need to export some variables for pipenv

```
export PIPENV_VENV_IN_PROJECT=1
export PIPENV_PYTHON=$PYENV_ROOT/shims/python
```
After setting those variables

```
pipenv install --dev
```

And now you can enter pipenv shell 

```
pipenv shell
```
In pipenv shell execute

```
pre-commit install
```
The last one is optional, but will help you, not letting you commit horrible code.

## Deployment

Make sure you have the requirements versions of the session before continue with this README.

Build the container:
```
$ docker-compose build
```

The project provides a script for restarting, after make any changes, and building one service that is introduce as a parameter:
```
./ compose-build.sh NAME_SERVICE
```
This execute:
```
docker-compose down
docker-compose build
...
docker-compose up NAME_SERVICE
```

Restart the service:
```
$ docker-compose down
$ docker-compose up 
```

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
