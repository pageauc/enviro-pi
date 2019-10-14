# Enviro-Pi
Monitor temperature, humidity, barometric pressure trends with a Raspberry Pi and SenseHat.
Data is stored to a sqlite3 database default every 300 seconds.  A webserver
allows viewing data status, charts and statistics from a web browser on your local network.

This project is a modified version originally from https://github.com/odlevakp/enviro-pi

### Quick Install
**IMPORTANT** - It is suggested you do a Raspbian ***sudo apt-get update*** and ***sudo apt-get upgrade***
before curl install.

***Step 1*** With mouse left button highlight curl command in code box below. Right click mouse in **highlighted** area and Copy.
***Step 2*** On RPI putty SSH or terminal session right click, select paste then Enter to download and run script.

    curl -L https://raw.github.com/pageauc/enviro-pi/master/setup.sh | bash

***To Run***

    cd ~/enviro-pi
    ./enviro-pi.sh install    
    ./enviro-pi.sh start
    
To Access enviro-pi web interface See ***./enviro-pi.sh*** HELP.   
From a computer on your local network, Type or copy/paste url link into web browser url box. 

### Hardware requirements
* Raspberry Pi 2, 3, 4  suggest using raspbian buster or stretch.   
* RPI SenseHat board   
* [40 pin GPIO Ribbon Cable](https://thepihut.com/products/gpio-ribbon-cable-for-raspberry-pi-40-pins) (optional)

If you put your SenseHat on top of your Pi, the temperature readings will be
inaccurate due to the heat coming from the pi - that's what the optional ribbon cable is for:

![SenseHat Ribbon Cable](http://files.phisolutions.eu/enviro-pi-hw1.jpg "SenseHat with Ribbon Cable")

To use your SenseHat with a ribbon cable, you can remove the GPIO header on the bottom of the hat. It won't go easy the first time, just remember, you are removing the bottom one ;-)

The application was inspired by the following resources:

* [Sense-hat API documentation](https://pythonhosted.org/sense-hat/)
* [w3schools](https://pythonhosted.org/sense-hat/) - for HTML menus, templates and CSS.
* [ChartJS](http://www.chartjs.org/docs) - Awesome charts used to display environment readings.
* [Flask](http://flask.pocoo.org/) - Web server used to display data, inspired by [this](https://github.com/pallets/flask/tree/master/examples/flaskr) blog example.
* [Python sqlite tutorial](http://zetcode.com/db/sqlitepythontutorial/)


### Manual Installation
Update your package database and make sure you have all required packages,
then clone this git repository. Installation of supervisor is optional, it
is used to keep the processes running in background.

```bash
sudo apt update
sudo apt install supervisor python3-flask sqlite3 git sense-hat
git clone https://github.com/odlevakp/enviro-pi.git ~/enviro-pi
```

### How to Auto Start
Supervisor was installed to keep your two processes alive. First one, `writer.py`, reads environmental information from sensehat and writes them into a database.
Second process, `webserver.py`, starts a web server and displays collected data. The configuration needed to run them using supervisor, is placed in the
supervisor subdirectory.

```bash
cd ~/enviro-pi

sudo ln -s /home/pi/enviro-pi/supervisor/* /etc/supervisor/conf.d/
sudo systemctl start supervisor.service

sudo supervisorctl
```

You should see both processes running and good to go.   
Open you browser on `http://RPI_IP_ADDRESS:8080`.  
eg http://192.168.1.145:8080


### Screenshots
![Status MacOS screenshot](http://files.phisolutions.eu/status.png "Status MacOS screenshot")
![Charts MacOS screenshot](http://files.phisolutions.eu/charts.png "Charts MacOS screenshot")
![Statistics Android screenshot](http://files.phisolutions.eu/statistics.png "Statistics Android screenshot")

### How to Query sqlite database
The writer process is storing environmental readings in a local SQLite database. You can use the CLI client
to make additional queries on the recorded dataset.


```sql
$ sqlite3 sensehat.db

sqlite> .headers on
sqlite> .mode column

sqlite> SELECT * FROM sensehat;

sqlite> SELECT MAX(humidity),
datetime(epoch, 'unixepoch', 'localtime') as date
FROM sensehat;
```

Please note that time is stored in the `epoch` column as time since epoch. Column `temp_prs` stores temperature from pressure, not used in the web interface.

### License and Authors
Copyright 2016 Pavol Odlevak

Using <a href="http://www.chartjs.org/">Chart.js</a> and <a href="http://momentjs.com/">Moment.js</a> available under the MIT license.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
