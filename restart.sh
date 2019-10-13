#!/bin/bash

echo "restarting webserver.py and writer.py"
sudo systemctl restart supervisor.service
echo "Bye"
