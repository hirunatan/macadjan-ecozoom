#!/bin/sh 
# Script to execute collectstatic in all sites in this server
for site in `cat ../tools/sites.txt | grep -v "^ *#.*"`; do 
    echo "################################" 
    echo $site
    export DJANGO_SETTINGS_MODULE="settings.${site}_pro"
    yes 'yes' | ./manage.py collectstatic
done 

