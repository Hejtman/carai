#!/bin/sh

rsync -e 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'  -La --exclude '.*' --exclude '__pycache__' --delete '../carai/' pi@192.168.10.1:'~/pi/carai'

