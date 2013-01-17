#!/bin/sh
# Script to create a backup of one site (both the mysql database and the configuration files)

if test "$1" = ""; then 
    echo "Usage: ./backup_site.sh <site_tag>"
    exit 1
fi

SITE_TAG=$1

SRC_DIR=../src
SETTINGS_FILE=${SRC_DIR}/settings/${SITE_TAG}.py
SETTINGS_PRO_FILE=${SRC_DIR}/settings/${SITE_TAG}_pro.py
ACTIVATE_FILE=${SRC_DIR}/activate_${SITE_TAG}.sh
ACTIVATE_PRO_FILE=${SRC_DIR}/activate_${SITE_TAG}_pro.sh
WHOOSH_DIR=${SRC_DIR}/whoosh/index_${SITE_TAG}
echo '.....->' 
echo "${SRC_DIR}/uwsgi_${SITE_TAG}.py"
if test -f "${SRC_DIR}/uwsgi_${SITE_TAG}.py"; then
    UWSGI_FILE=${SRC_DIR}/uwsgi_${SITE_TAG}.py
else
    UWSGI_FILE=""
fi
if test -d "${SRC_DIR}/skins/${SITE_TAG}"; then
    SKIN_DIR=${SRC_DIR}/skins/${SITE_TAG}
else
    SKIN_DIR=""
fi

BACKUP_FILE=backups/backup_${SITE_TAG}.tgz
DB_DUMP_FILE=dump_${SITE_TAG}.sql

DB_NAME_TMP=`grep "'NAME':" $SETTINGS_FILE | cut -d "'" -f 4`
DB_NAME=`echo $DB_NAME_TMP | cut -d ' ' -f 1`
DB_USER_TMP=`grep "\['USER'\]" $SETTINGS_PRO_FILE | cut -d "'" -f 4`
DB_USER=`echo $DB_USER_TMP | cut -d ' ' -f 1`
DB_PASSWORD_TMP=`grep "\['PASSWORD'\]" $SETTINGS_PRO_FILE | cut -d "'" -f 4`
DB_PASSWORD=`echo $DB_PASSWORD_TMP | cut -d ' ' -f 1`
DB_HOST_TMP=`grep "\['HOST'\]" $SETTINGS_PRO_FILE | cut -d "'" -f 4`
DB_HOST=`echo $DB_HOST_TMP | cut -d ' ' -f 1`

if ! test "$DB_HOST" = ""; then 
    mysqldump -u$DB_USER --password=$DB_PASSWORD -h$DB_HOST $DB_NAME > $DB_DUMP_FILE
else
    mysqldump -u$DB_USER --password=$DB_PASSWORD $DB_NAME > $DB_DUMP_FILE
fi

tar cvfz $BACKUP_FILE $DB_DUMP_FILE $SETTINGS_FILE $SETTINGS_PRO_FILE $ACTIVATE_FILE $ACTIVATE_PRO_FILE $WHOOSH_DIR $UWSGI_FILE $SKIN_DIR

rm $DB_DUMP_FILE

