#!/bin/sh
# Script to dump classification lists to a json file
./manage.py dumpdata macadjan.EntityType macadjan.Category macadjan.SubCategory --indent=4 > classification.json

