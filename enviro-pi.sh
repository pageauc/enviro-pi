#!/bin/bash
# enviro-pi.sh is a systemctl script to control webserver.py and writer.py
# written by Claude Pageau  https://github.com/pageauc/enviro-p
version="1.2"

echo "$0 ver $version  written by Claude Pageau"
echo "Control enviro-pi webserver.py and writer.py"
echo ""

if [ "$1" = "start" ]; then
    echo "Start: sudo systemctl start supervisor.service"
    sudo systemctl start supervisor.service
    echo "Wait 10 seconds for supervisor sevices to start"
    sleep 10
elif [ "$1" = "stop" ]; then
    echo "Stop: sudo systemctl stop supervisor.service"
    sudo systemctl stop supervisor.service
elif [ "$1" = "install" ]; then
    # Run this option to initialize supervisor.service for enviro-pi
    echo "Install: sudo ln -s /home/pi/enviro-pi/supervisor/* /etc/supervisor/conf.d/"
    sudo ln -s /home/pi/enviro-pi/supervisor/* /etc/supervisor/conf.d/
    if [ $? == 0 ]; then
        echo "INFO  - Done Install."
    else
        echo "WARN  - Already Installed."
    fi
    echo ""
    echo "INFO  - To Start enviro-pi supervisor service"
    echo "        Run this script again with start Option]"
elif [ "$1" = "upgrade" ]; then
    echo "Upgrade: Run setup.sh from https://github.com/pageauc/enviro-pi"
    curl -L https://raw.github.com/pageauc/enviro-pi/master/setup.sh | bash
    exit 0
else
   echo "Usage: ./enviro-pi.sh [Option]"
   echo ""
   echo "Options:"
   echo "  start      Start supervisor service"
   echo "  stop       Stop supervisor service"
   echo "  install    Install symbolic links for supervisor service"
   echo "  upgrade    Upgrade files from Github Repo"
   echo "  help       Display Usage message and Status"
   echo ""
   echo "Example:  ./enviro-pi.sh start"
fi

echo ""
echo "Status:"
sleep 2  # Allow time for service changes

if [ -z "$( pgrep -f webserver.py )" ]; then
   echo "INFO  - webserver.py is NOT Running"
else
   webPID=$(pgrep -f webserver.py)
   echo "INFO  - webserver.py is RUNNING PID $webPID"
fi

if [ -z "$( pgrep -f writer.py )" ]; then
   echo "INFO  - writer.py is NOT Running"
else
   writePID=$(pgrep -f writer.py)
   echo "INFO  - writer.py is RUNNING PID $writePID"
fi

echo ""
myip1=$(hostname -I | cut -d " " -f 1)
myip2=$(hostname -I | cut -d " " -f 2)
echo "HELP  - To Access RUNNING enviro-pi web interface"
echo "        Type or copy/paste url link below"
echo "        into web browser url window. Normally near top of browser app."
echo ""
echo "        Example: http://$myip1:8080"
echo "                 http://$myip2:8080"
echo ""
echo "Bye"
