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
## User interest(Optional)
If you are getting this error, `docker : /bin/sh^M: bad interpreter: No shu file or directory`
You would like to see this page to solve it: https://forums.docker.com/t/error-while-running-docker-code-in-powershell/34059

Other thing that might be useful is restarting docker, that may solve some troubles of network.

```
$ docker-machine restart
```
