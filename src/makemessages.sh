#!/bin/bash
echo "macadjan_ecozoom................"
cd macadjan_ecozoom
../manage.py makemessages --all
../manage.py compilemessages

echo "macadjan_form................"
cd ../macadjan_form
../manage.py makemessages --all
../manage.py compilemessages

echo "macadjan_importer................"
cd ../macadjan_importer
../manage.py makemessages --all
../manage.py compilemessages

echo "macadjan_sync................"
cd ../macadjan_sync
../manage.py makemessages --all
../manage.py compilemessages

