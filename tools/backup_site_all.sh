#!/bin/sh 
# Script to backup all sites in this server
for site in `cat sites.txt | grep -v "^ *#.*"`; do 
    echo "################################" 
    echo $site
    sh ./backup_site.sh $site 2>&1 
done 

