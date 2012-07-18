#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

settings_name = os.environ.get('DJANGO_SETTINGS_MODULE', None)
if not settings_name:
    sys.stderr.write("Error: you must set DJANGO_SETTINGS_MODULE variable by calling 'source activate_xxx.sh'.\n")
    sys.exit(1)

try:
    settings = __import__(settings_name, fromlist=['settings'])
except ImportError:
    sys.stderr.write("Error: can't find %s module.\n" % settings_name)
    sys.exit(1)

from django.core.management import execute_manager
if __name__ == "__main__":
    execute_manager(settings)

