#!/bin/bash
# speed-install.sh script written by Claude Pageau 1-Jul-2016

<<<<<<< HEAD
ver="1.4"
=======
ver="2.0"
>>>>>>> c8ca8f2600eef9bf349ffc5ec6dfcd71d4c04f1d
INSTALL_DIR='enviro-pi'  # Default folder install location

cd ~   # change to users home directory
# Remember where this script was launched from
HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# List of files to copy to destination RPI using wget
enviro_files=("README.md" "LICENSE" "enviro-web.py" "enviro-pi.py" "run.sh" \
"static/Chart.min.js" "static/favicon.ico" "static/menu.js" \
"static/moment.min.js" "static/raspberry_pi_logo.png" "static/style.css" \
"supervisor/enviro-web.conf" "supervisor/enviro-pi.conf" \
"templates/statistics.html" "templates/charts.html" "templates/statistics.html" "templates/status.html")

echo "-----------------------------------------------"
echo "enviro-pi setup.sh ver $ver"
echo "-----------------------------------------------"
echo "Download GitHub Files to $INSTALL_DIR"

mkdir -p $INSTALL_DIR
cd $INSTALL_DIR
mkdir -p static
mkdir -p supervisor
mkdir -p templates

for fname in "${enviro_files[@]}" ; do
    wget_output=$(wget -O $fname -q --show-progress https://raw.github.com/pageauc/enviro-pi/master/$fname)
    if [ $? -ne 0 ]; then
        wget -O $fname https://raw.github.com/pageauc/enviro-pi/master/$fname
        if [ $? -ne 0 ]; then
            echo "ERROR - $fname wget Download Failed. Check Internet Connection"
        fi
    fi
done

wget -O templates/about.html -q https://raw.github.com/pageauc/enviro-pi/master/templates/about.html

if [ -f config.py ]; then     # check if local file exists.
    wget -O config.py.new -q --show-progress https://raw.github.com/pageauc/enviro-pi/master/config.py
else
    wget -O config.py -q --show-progress https://raw.github.com/pageauc/enviro-pi/master/config.py
fi


echo "-----------------------------------------------"
echo "Install Dependencies.  Wait ..."
echo "-----------------------------------------------"
sudo apt install -yq supervisor
sudo apt install -yq python3-flask
sudo apt install -yq sqlite3
sudo apt install -yq sense-hat
sudo apt install -yq dos2unix
sudo apt install -yq python3-paho-mqtt

dos2unix *py
dos2unix *sh
chmod +x *.py
chmod -x config.py
chmod +x *.sh

cd $HOME_DIR

echo "
-----------------------------------------------
Install Complete
-----------------------------------------------
1. Ensure RPI sensehat is installed and working
2. Test enviro-pi

    cd ~/enviro-pi
    ./enviro-pi.py

    ./run.sh install
    ./run.sh start
    ./run.sh status

Access enviro-pi web interface per instructions.
Refresh Status page to display sensehat data and confirm system is working.

$INSTALL_DIR version $ver
Good Luck Claude ...
Bye"
