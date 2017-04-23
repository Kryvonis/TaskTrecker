#!/usr/bin/env bash

sudo mkdir venv
sudo virtualenv -p python3 venv
. $(pwd)/venv/bin/activate
sudo pip install -r $(pwd)/requirements.txt
sudo cp /src/settings/local.sample.py /srv/www/IgoStories/igostories/settings/local.py
python manage.py makemigrations
python manage.py migrate
sh scripts/run.sh