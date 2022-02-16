#!/bin/bash
sudo apt-get update -y &> /dev/null
sleep 1
aws --version &> /dev/null
if [ $? != "0" ] ; then
    sudo apt-get install awscli -y &> /dev/null 
else 
    echo 'aws-cli is already installed'
    sleep 3
fi