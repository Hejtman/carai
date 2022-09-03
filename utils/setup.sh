#!/bin/sh

git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install
cd ..
sudo apt install espeak
