#!/bin/bash

SERIE_URL="multi_object"
SERIE_ID=54641

ROOT="/home/dfelinto/src/tools/task-forces"
CONDUIT="/home/dfelinto/.conduit-dev.b.o"
GRAFISTA="/home/dfelinto/src/tools/grafista"

cd $ROOT
source venv/bin/activate
remaining=$(python task_force_remaining.py ${SERIE_ID} `cat $CONDUIT`)

cd $GRAFISTA
source venv/bin/activate
cd grafista
python manage.py insert_sample $SERIE_URL $remaining
