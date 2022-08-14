#!/bin/sh

wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz
tar -zxvf Python-3.10.2.tgz
cd Python-3.10.2
./configure --enable-optimizations
sudo apt update
sudo apt install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
Compile Python
sudo make altinstall

cd /usr/bin
sudo rm python3
sudo ln -s /usr/local/bin/python3.10 python3

