# Enviro-Pi
Monitor temperature, humidity, barometric pressure trends with a Raspberry Pi and SenseHat.
Data is stored in a sqlite3 database. Default updates are every 5 minutes.  

A webserver allows viewing data trends status, charts and statistics from a web browser on your local network.

Includes optional feature to upload data to the Weather Underground Personal Weather Station web site.

This project is a modified version originally from https://github.com/odlevakp/enviro-pi

### Quick Install
**IMPORTANT** - It is suggested you do a Raspbian ***sudo apt-get update*** and ***sudo apt-get upgrade***
before curl install.  You should have a recent RPI OS distro.  Bullseye or later.

***Step 1*** With mouse left button press copy icon on right side of box below.
***Step 2*** On RPI putty SSH or terminal session right click, select paste then Enter to download and run script.

    curl -L https://raw.github.com/pageauc/enviro-pi/master/setup.sh | bash

This will install and setup the ~/enviro-pi directory

### To Run/Test
From SSH or Terminal Session input the following command to test run enviro-pi.py.

    cd ~/enviro-pi
    ./enviro-pi.py
    
Monitor log activity to ensure correct operation. Note if sense hat display is enabled red up arrow indicates
temp rise since last reading. blue down arrow temperature decrease.  Red/blue stripes no change.  The pixel
in the top left indicates upload status. Green last upload successful. Red last upload failed.    
    
### Setup enviro-pi.py and weather.py as background tasks 
    
    ./enviro-pi.sh install
    ./enviro-pi.sh help
    ./enviro-pi.sh status
    
Example of Help screen below For more information on supervisor [See Docs](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps)
 
```
./enviro-pi.sh ver 2.0 written by Claude Pageau
Control enviro-pi webserver.py and enviro-pi.py

Usage: ./enviro-pi.sh [Option]

Options:
  start      Start supervisor service
  stop       Stop supervisor service
  status     status of supervisor service
  install    Install symbolic links for supervisor service
  upgrade    Upgrade files from Github Repo
  help       Display Usage message and Status
```
    
#### Note   
***./enviro-pi.sh install*** command above will setup systemd supervisor symbolic links.   
This will auto start webserver.py and enviro-pi.py on boot.
See enviro-pi.sh help for other options. Eg start, stop, upgrade.  Reboot to test autostart.

### Web Interface 
To Access enviro-pi web interface See ***./enviro-pi.sh*** help.      

From a computer on your local network, Type or copy/paste url link into web browser url box.     

#### On the Enviro-Pi Web Page
Press top menu ***Status*** button to view current data. Press ***Refresh Page*** button to update data.    
If no data displayed check sensehat hardware and setup.

After startup, allow 15-20 minutes to accumulate chart data (default updates are every 5 minutes).   
Press ***Charts*** button to display historical data, Press green box pull down to select time range,    
then     
Press ***Load Charts*** button to update graphs for selected range.
Graphs will update automatically after that but you can always refresh with the ***Load Charts*** button

### Setup Weather Underground Personal Weather Station 

enviro-pi.py has an optional feature to upload your data to the Weather Undergound Personal Weather Station.
To setup your Raspberry Pi and Sense Hat to upload data

* Create/login to an account at https://www.wunderground.com/login?action=member-devices
* Add New Device and select Raspberry Pi from pulldown.
* Setup device name and location per web site instuctions.
* When device registration is complete you will receive a Station ID and a Station Key.
* login to your raspberry pi and cd to enviro-pi folder.
* nano config.py and edit weather station settings to add your Station ID and Key.
* Edit STATION_UPLOAD_ON = True
* Ctrl-x y to save changes and exit nano

To test

    ./enviro-pi.sh stop
    ./enviro-pi.py
    
Review logs to ensure uploads are successful.
If OK restart enviro-pi.py and weather.py 

    ./enviro-pi.sh start
    

### Hardware Requirements
* [Raspberry Pi](https://www.raspberrypi.org/products/) 2, 3, 4  suggest using Raspbian Buster or Stretch.   
* [RPI SenseHat board](https://www.raspberrypi.org/products/sense-hat/)   
* [40 pin GPIO Ribbon Cable](https://thepihut.com/products/gpio-ribbon-cable-for-raspberry-pi-40-pins) (optional)

If you put your SenseHat on top of your Pi, the temperature readings will be
inaccurate due to the heat coming from the pi - that's what the optional ribbon cable is for:
To use your SenseHat with a ribbon cable, you can carefully remove the GPIO header on the bottom of the hat.
It won't go easy the first time, just remember, you are removing the bottom one ;-)
![SenseHat Ribbon Cable](http://files.phisolutions.eu/enviro-pi-hw1.jpg "SenseHat with Ribbon Cable")

### Edit Configuraton
User Variables are stored in the config.py file.  Edit this file to change variables per comments

    cd ~/enviro-pi
    nano config.py

Press ctrl-x y to exit and save nano changes.

### Screenshots
![Status MacOS screenshot](http://files.phisolutions.eu/status.png "Status MacOS screenshot")
![Charts MacOS screenshot](http://files.phisolutions.eu/charts.png "Charts MacOS screenshot")
![Statistics Android screenshot](http://files.phisolutions.eu/statistics.png "Statistics Android screenshot")

### How to Query sqlite database
The writer process is storing environmental readings in a local SQLite database. You can use the CLI client
to make additional queries on the recorded dataset.

```
cd ~/enviro-pi
sqlite3 enviro-pi.db

sqlite> .headers on
sqlite> .mode column

sqlite> SELECT * FROM sensehat;

sqlite> SELECT MAX(humidity),
datetime(epoch, 'unixepoch', 'localtime') as date
FROM sensehat;
```
ctrl-d to exit sqlite3 console.   

***Note*** Time is stored in the `epoch` column as time since epoch. 
Column `temp_prs` stores temperature from pressure, not used in the web interface.

### License and Authors
Copyright 2016 Pavol Odlevak

Using <a href="http://www.chartjs.org/">Chart.js</a>     
and <a href="http://momentjs.com/">Moment.js</a> available under the MIT license.

The application was inspired by the following resources:

* [Sense-hat API documentation](https://pythonhosted.org/sense-hat/)
* [w3schools](https://pythonhosted.org/sense-hat/) - for HTML menus, templates and CSS.
* [ChartJS](http://www.chartjs.org/docs) - Awesome charts used to display environment readings.
* [Flask](http://flask.pocoo.org/) - Web server used to display data, inspired by [this](https://github.com/pallets/flask/tree/master/examples/flaskr) blog example.
* [Python sqlite tutorial](http://zetcode.com/db/sqlitepythontutorial/)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
