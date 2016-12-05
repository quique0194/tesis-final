#!/bin/bash

sudo apt-get update
sudo apt-get install -y git build-essential python-dev

# install pip
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
sudo python get-pip.py

sudo pip install numpy pygame theano ipython pillow
