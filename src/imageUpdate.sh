#!/bin/bash

USER='frogmon'
PASS='Rhlrnf8359!'
HOST='frogmon.synology.me'
PORT=9122
LOCAL_FILE=$1
REMOTE_PATH='/photo/TIMELAPSEs/frogmon/timelapses'

if [ $# -ne 1 ]; then
    echo "Usage: $0 <local_file_path>"
    exit 1
fi

if [ ! -f $LOCAL_FILE ]; then
    echo "Error: File $LOCAL_FILE does not exist."
    exit 1
fi

/usr/bin/expect << EOF
spawn /usr/bin/sftp -oPort=$PORT $USER@$HOST
expect "password:"
send "$PASS\r"
expect "sftp>"
send "put $LOCAL_FILE $REMOTE_PATH\r"
expect "sftp>"
send "bye\r"
EOF
