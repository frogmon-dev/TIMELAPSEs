#!/bin/bash

USER='frogmon'
PASS='Rhlrnf8359!'
HOST='frogmon.synology.me'
PORT=9122
TODAY=$(date '+%Y%m%d')
REMOTE_PATH='/photo/TIMELAPSEs/frogmon/times01'
DELETE_PATH='/home/pi/TIMELAPSEs/images'
ZIPFILE="${DELETE_PATH}/${TODAY}_images.zip"

zip -r "${ZIPFILE}" "${DELETE_PATH}/image${TODAY}"* && rm "${DELETE_PATH}/image${TODAY}"*

/usr/bin/expect << EOF
spawn /usr/bin/sftp -oPort=$PORT $USER@$HOST
expect "password:"
send "$PASS\r"
expect "sftp>"
send "put $ZIPFILE $REMOTE_PATH\r"
expect "sftp>"
send "bye\r"
EOF

if [ $? -eq 0 ]; then
    rm $ZIPFILE
else
    echo "Error occurred during sftp transfer"
fi
