#!/bin/bash
# speed-install.sh script written by Claude Pageau 1-Jul-2016

ver="1.0"
INSTALL_DIR='enviro-pi'  # Default folder install location

cd ~   # change to users home directory
# Remember where this script was launched from
HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# List of files to copy to destination RPI using wget
enviro_files=("README.md" "LICENSE" "webserver.py" "writer.py" "restart.sh" \
"static/Chart.min.js" "static/favicon.ico" "static/menu.js" \
"static/moment.min.js" "static/raspberry_pi_logo.png" "static/style.css" \
"supervisor/enviro-pi-webserver.conf" "supervisor/enviro-pi-writer.conf" \
"templates/statistics.html" "templates/charts.html" "templates/statistics.html" "templates/status.html")

echo "-----------------------------------------------"
echo "enviro-pi setup.sh ver $ver"
echo "-----------------------------------------------"
echo "Download GitHub Files to $INSTALL_DIR"

mkdir $INSTALL_DIR
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

echo "-----------------------------------------------"
echo "Install Dependencies.  Wait ..."
echo "-----------------------------------------------"
sudo apt-get install -yq supervisor
sudo apt-get install -yq python3-flask
sudo apt-get install -yq sqlite3
sudo apt-get install -yq sense-hat

chmod +x *.py
chmod +x *.sh
cd $HOME_DIR

echo "
-----------------------------------------------
Install Complete
-----------------------------------------------
1. Ensure RPI sensehat is installed and working
2. Raspberry pi optionally needs a monitor/TV attached to display openCV window
3. Run speed-cam.py in SSH Terminal (default) or optional GUI Desktop
   Review and modify the config.py settings as required using nano editor
4. To start speed-cam open SSH or a GUI desktop Terminal session
   and change to speed-camera folder and launch per commands below

   cd ~/enviro-pi
   ./start.sh

$INSTALL_DIR version $ver
Good Luck Claude ...
Bye"
