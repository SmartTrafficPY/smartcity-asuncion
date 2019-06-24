# SmartTraffic-SmartCityAsuncion
La plataforma del servidor del proyecto SmartTraffic

## INSTALL
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

## Deployment
First of all, you need to put some environments variables in a `.env` named file inside the `postgres-db` directory, containing the following:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
POSTGRES_DB=smarttraffic
``` 

Build the container:
```
$ docker-compose build
```

Build the static files and populate the volume with them:
```
$ docker-compose run
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

##PRODUCTION
Before you run in production, check the output of:

```
$ python manage.py check --deploy
```

##User interest(Optional)
If you are getting this error, `docker : /bin/sh^M: bad interpreter: No shu file or directory`
You would like to see this page to solve it: https://forums.docker.com/t/error-while-running-docker-code-in-powershell/34059

Other thing that might be useful is restarting docker, that may solve some troubles of network.

```
$ docker-machine restart
```

###Migration of the DB
If you want to migrate the models that you are adding to the project to the postgres DB,
you need to migrate it inside of the django-server container. You enter to the bash of it with the following command:

```
$ docker container exec -it <container_id> /bin/bash 
```

 
