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
Build the container:
```
$ docker-compose build
```

Build the static files and populate the volume with them:
```
$ docker-compose run
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