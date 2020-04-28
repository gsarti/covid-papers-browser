#!/bin/bash

#install compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose;
sudo chmod +x /usr/local/bin/docker-compose;

# add repo nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID);
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - ;
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list ;

#install nvidia runtime
sudo apt-get update && sudo apt-get install -y nvidia-docker2;
sudo systemctl restart docker;






