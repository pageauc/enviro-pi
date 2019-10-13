#!/bin/bash
#  systemctl script for enviro-pi webserver.py and writer.py

echo "$0"
echo ""
if [ "$1" = "start" ]; then
    echo "sudo systemctl start supervisor.service"
    sudo systemctl start supervisor.service
elif [ "$1" = "stop" ]; then
    echo "sudo systemctl stop supervisor.service"
    sudo systemctl stop supervisor.service
else
   echo "HELP"
   echo "===="
   echo "Specify a parameter start or stop"
   echo "Eg"
   echo "    ./enviro-pi.sh start"
   echo ""
   echo "No parameter shows status"
fi
sleep 3  # wait for any service changes

echo ""
echo "STATUS"
echo "======"
if [ -z "$( pgrep -f webserver.py )" ]; then
   echo "webserver.py is NOT Running"
else
   webPID=$(pgrep -f webserver.py)
   echo "webserver.py is RUNNING PID $webPID"
fi

if [ -z "$( pgrep -f writer.py )" ]; then
   echo "writer.py is NOT Running"
else
   writePID=$(pgrep -f writer.py)
   echo "writer.py is RUNNING PID $writePID"
fi

echo ""
echo "This RPI's IP Addresses"
myip=$(hostname -I | cut -d " " -f 1)
echo "$myip"
hostname -I | cut -d " " -f 2
hostname -I | cut -d " " -f 3
echo "To Access RUNNING enviro-pi web interface. Type or paste url link below"
echo "into web browser url window. Normally near top of browser app."
echo "http://$myip:8080"
echo ""
echo "Bye"
