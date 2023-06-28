#!/usr/bin/bash

docker-compose up -d
nohup /home/glozada/.cache/pypoetry/virtualenvs/backend-hQ8bC7ni-py3.10/bin/python /home/glozada/Documents/Projects/HOTBOX/backend/gui/main.py

# SUBSTITUTE PYTHON PATH WITH THE ONE ON THE RASPBERRY PI. TO GET THE PYTHON PATH DO THE FOLLOWING:
# > poetry shell
# > which python

# SUBSTITUTE main.py path with the one in the raspberry.

# Create a file at /lib/systemd/system/hotbox-gui.service with sudo permission. Add the following (substituting the path
# for start-gui.sh with the one in the raspberry:

#[Unit]
#Description=HotBox GUI and DB
#
#[Service]
#ExecStart=/home/glozada/Documents/Projects/HOTBOX/backend/start-gui.sh
#
#[Install]
#WantedBy=multi-user.target

# Execute these commands in the terminal:
# > sudo systemctl daemon-reload
# > sudo systemctl enable --now hotbox-gui.service
