#!/bin/bash
if [ $# -eq 0 ]
  then
    python3 src/parking_lot.py
else
    if [ -e $1 ]
    then
        python3 src/parking_lot.py $1
    else
        echo "$1 File not exists"
    fi
fi