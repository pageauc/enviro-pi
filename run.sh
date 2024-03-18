#!/bin/bash
# run.sh is a systemctl script to control webserver.py and writer.py
# written by Claude Pageau  https://github.com/pageauc/enviro-p
version="2.0"
programs="enviro-pi.py enviro-web.py"
params="start, stop, restart, status, install, uninstall"

echo "$0 ver $version  written by Claude Pageau"
echo "Control $programs"
echo ""

if [ "$1" = "start" ]; then
    echo "sudo supervisorctl start enviro-pi enviro-web"
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start enviro-pi enviro-web
    echo "Wait 10 seconds for supervisor services to start"
    sleep 10
    sudo supervisorctl status all
elif [ "$1" = "stop" ]; then
    echo "STOP: sudo supervisorctl stop enviro-pi enviro-web"
    sudo supervisorctl stop enviro-pi enviro-web
    sudo supervisorctl status all
    exit 0
elif [ "$1" = "status" ]; then
    echo "STATUS: sudo supervisorctl status all"
    sudo supervisorctl status all
    exit 0
elif [ "$1" = "install" ]; then
    # Run this option to initialize supervisor.service
    echo "INSTALL: sudo ln -s /home/pi/enviro-pi/supervisor/* /etc/supervisor/conf.d/"
    sudo ln -s /home/pi/enviro-pi/supervisor/* /etc/supervisor/conf.d/
    if [ $? == 0 ]; then
        echo "INFO  - Done Install."
    else
        echo "WARN  - Already Installed."
        exit 0
    fi
    exit 0
elif [ "$1" = "uninstall" ]; then
    sudo supervisorctl stop enviro-pi enviro-web
    sudo rm /etc/supervisor/conf.d/enviro-pi.conf /etc/supervisor/conf.d/enviro-web.conf
    echo "Uninstall Finished"
    exit 0

elif [ "$1" = "upgrade" ]; then
    echo "Upgrade program files from github repo"
    echo " curl -L https://raw.github.com/pageauc/enviro-pi/master/setup.sh | bash "
    curl -L https://raw.github.com/pageauc/enviro-pi/master/setup.sh | bash
    exit 0
else
   echo "Usage: ./run.sh [Option]"
   echo ""
   echo "Options:"
   echo "  start        Start supervisor service"
   echo "  stop         Stop supervisor service"
   echo "  status       Status of supervisor service"
   echo "  install      Install symbolic links for supervisor service"
   echo "  uninstall    Uninstall symbolic links for supervisor service"
   echo "  upgrade      Upgrade files from Github Repo"
   echo "  help         Display Usage message and Status"
   echo ""
   echo "Example:  ./run.sh status"
   exit 0
fi

echo ""
myip1=$(hostname -I | cut -d " " -f 1)
myip2=$(hostname -I | cut -d " " -f 2)
echo "Status" 
echo ""
echo " To Access RUNNING enviro-pi web interface"
echo "    Type or copy/paste url link below"
echo "    into web browser url window. Normally near top of browser app."
echo ""
echo "    Example: http://$myip1:8080"
echo ""
echo "Bye"
