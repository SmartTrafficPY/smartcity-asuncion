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

