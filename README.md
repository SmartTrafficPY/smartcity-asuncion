# SmartTraffic-SmartCityAsuncion
La plataforma del servidor del proyecto SmartTraffic

## INSTALL

Python: 3.7 or +

Check that you have the correct python version:
```
$ cat .python-version
3.7.0
$ python -V
Python 3.7.0
```

## Deployment
Build the container:
```
$ docker-compose build
```

Build the static files and populate the volume with them:
```
$ docker-compose -f docker/compose/smwebsite/docker-compose.yml run smwebsite
```

Restart the service:
```
$ docker-compose down
$ docker-compose up 
```

You'll find the app is running on http://127.0.0.1:8000
or the docker VM if you are running in docker toolbox, that might be 192.168.99.100:8000