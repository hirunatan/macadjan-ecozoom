#!/bin/sh
# Script to dump the SiteInfo to a json file
./manage.py dumpdata macadjan.SiteInfo --indent=4 > siteinfo.json

