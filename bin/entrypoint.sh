#!/bin/bash

# detect userid:groupid of contents of data folder
SUITEDCONNECTORS_ROOT="${SUITEDCONNECTORS_ROOT:-/opt/suitedconnectors.poker}"
DATA_DIR="${DATA_DIR:-/opt/suitedconnectors.poker/data}"
DJANGO_USER="${DJANGO_USER:-www-data}"

# Autodetect UID and GID of host user based on ownership of files in the volume
USID=$(stat --format="%u" "$DATA_DIR")
GRID=$(stat --format="%g" "$DATA_DIR")
COMMAND="$*"

# run django as the host user's uid:gid so that any files touched have the same permissions as outside the container
# e.g. ./manage.py runserver

if [[ "$USID" != 0  &&  "$GRID" != 0 ]]; then
    chown "$USID":"$GRID" "$DATA_DIR"
    chown -R "$USID":"$GRID" "$DATA_DIR/logs"
    chown -R "$USID":"$GRID" "$SUITEDCONNECTORS_ROOT/core"
    usermod -u "$USID" "$DJANGO_USER"
    groupmod -g "$GRID" "$DJANGO_USER"
else
    chown -R "$DJANGO_USER":"$DJANGO_USER" "$DATA_DIR"
    chown -R root:root "$DATA_DIR/redis"
    chown -R "$DJANGO_USER":"$DJANGO_USER" "$SUITEDCONNECTORS_ROOT/core"
fi
gosu "$DJANGO_USER" bash -c "$COMMAND"
