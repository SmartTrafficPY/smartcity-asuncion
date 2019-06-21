#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

## create databases
#if not exists...
if psql -lqt | cut -d \| -f 1 | grep -qw smarttraffic
then
    echo Database already exists
else
    psql -c "CREATE DATABASE smarttraffic;"
fi

# add extensions to databases
psql smarttraffic -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql smarttraffic -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"
psql smarttraffic -c "CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;"
psql smarttraffic -c "CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;"
psql smarttraffic -c "CREATE EXTENSION IF NOT EXISTS hstore;"


#add osm data to the database...
osm2pgsql --create --slim \
    --database smarttraffic \
    --style /osm/openstreetmap-carto/openstreetmap-carto.style --multi-geometry \
    /osm/paraguay-latest.osm.pbf

#2 causes 2 CPU cores to be used.
#    --cache 1000 --number-processes 2 --hstore \

#tells what columns to create with the style
#create multi-geometry
#the last line is the path to the map