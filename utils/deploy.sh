#!/bin/sh

ping -t 1 -c 1 192.168.1.238 >/dev/null 2>&1 && rsync -e 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'  -La --exclude '.*' --exclude '__pycache__' --delete '../carai/' pi@192.168.1.238:'/home/pi/carai' || rsync -e 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'  -La --exclude '.*' --exclude '__pycache__' --delete '../carai/' pi@192.168.10.1:'/home/pi/carai'

