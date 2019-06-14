#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

# create databases
psql -c "CREATE DATABASE gis;"

# add extensions to databases
psql gis -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql gis -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"
psql gis -c "CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;"
psql gis -c "CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;"

## restore database if dump file exists
#if [ -f /opt/backups/restore.dump ]; then
#  echo "Restoring backup..."
#  pg_restore -d gis --clean --if-exists /opt/backups/restore.dump
#fi