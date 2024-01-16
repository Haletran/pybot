#!/bin/bash

sudo curl -O code.deb https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64
sudo dpkg -i code.deb
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
