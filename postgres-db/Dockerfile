FROM postgres:10
##MAINTAINER Joaquin Olivera <joaquin.olivera@edu.uc.py>

ENV POSTGIS_MAJOR 2.5
ENV POSTGIS_VERSION 2.5.2+dfsg-1~exp1.pgdg90+1
#ENV TZ America/New_York

## add addressing dictionary
#RUN mkdir -p /opt/apps
#COPY ./pgsql-address-dictionary.zip /opt/apps/pgsql-address-dictionary.zip

#add osm2pgsql for exporting OSM data...
RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION \
           osm2pgsql \
           osmctools \
      && rm -rf /var/lib/apt/lists/*

# set time zone
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#add OSM styles and paraguay maps...
RUN mkdir -p /osm
COPY ./osm/paraguay-latest.osm.pbf /osm/paraguay-latest.osm.pbf
COPY ./osm/openstreetmap-carto/openstreetmap-carto.style /osm/openstreetmap-carto/openstreetmap-carto.style
# add init script
RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
COPY ./update-postgis.sh /usr/local/bin

