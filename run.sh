#!/bin/bash
export DB_HOST='localhost'
export DB_PORT=3306
export DB_USER='admin'
export DB_PASSWORD='12345'
export DB_NAME='parking'

if [ $# -eq 0 ]
  then
    FLASK_APP=src/app.py flask run
else
    if [ -e $1 ]
    then
        python3 src/parking_lot.py $1
    else
        echo "$1 File not exists"
    fi
fi