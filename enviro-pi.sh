#!/bin/bash
#  systemctl script for enviro-pi webserver.py and writer.py

echo "$0"
echo ""
if [ "$1" = "start" ]; then
    sudo systemctl start supervisor.service
elif [ "$1" = "stop" ]; then
    sudo systemctl stop supervisor.service
elif [ "$1" = "restart" ]; then
    sudo systemctl restart supervisor.service
else
   echo "     HELP"
   echo "     ----"
   echo "Specify parameter start, stop or restart"
   echo "Eg"
   echo "    ./enviro-pi.sh restart"
   echo ""
fi

sleep 2  # wait for any service changes

if [ -z "$( pgrep -f webserver.py )" ]; then
   echo "WARN   - webserver.py is NOT Running"
else
   webPID=$(pgrep -f webserver.py)
   echo "STATUS - webserver.py is Running PID $webPID"
fi

if [ -z "$( pgrep -f writer.py )" ]; then
   echo "WARN   - writer.py is NOT Running"
else
   writePID=$(pgrep -f writer.py)
   echo "STATUS - writer.py is Running PID $writePID"
fi
echo ""
echo "------------------"
echo "$0 Bye"
