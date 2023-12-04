#!/bin/bash
# check if python3 exists
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found"
    exit
fi

UPLOAD_SCRIPT=scripts/upload.py
if [ ! -f "$UPLOAD_SCRIPT" ]; then
    echo "$UPLOAD_SCRIPT does not exist."
    exit
fi

# check if conf.json exists
CONF_FILE=conf.json
if [ ! -f "$CONF_FILE" ]; then
    echo "$CONF_FILE does not exist."
    exit
fi

HADOOP_USER_NAME="root" python3 $UPLOAD_SCRIPT --conf $CONF_FILE