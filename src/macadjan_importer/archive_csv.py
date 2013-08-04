# -*- coding: utf-8 -*-

import os.path
import csv

from django.utils.translation import ugettext as _

from .archive_base import EntityArchive

class EntityArchiveCSV(EntityArchive):
    '''
    Subclass of EntityArchive that uses a csv file as the entity archive.

    The csv will use the default dialect and the ; separator (this is the default when
    exporting from Excel or OpenOffice/LibreOffice).

    To allow to set many categories to an item, you can use several csv rows for the same
    item. The additional rows will have all columns empty except of the category columns.
    To check for emtpy rows we use the name column. For this, before start reading you
    must give the labels of the columns with the name and category.

    Upgrade: now any column except name may have multiple values: if there are more than
    one, the value will be converted to a list. The special treatment for categories is
    left as is, because it always converts them to list and so we maintain backwards
    compatibility.

    Also, the text is converted to utf-8 format if it's plain text, and trailing spaces
    are stripped.
    '''

    def __init__(self, filename):
        '''
        Open the file (specify the full path) and create a CSV reader with it.
        '''
        self.category_column_name = None
        self.name_column_name = None
        self.filename = filename
        self.csv_file = open(filename, 'rb')
        self.reader = csv.DictReader(self.csv_file, delimiter=',')
        self._index = 1 # skip initial header line
        self._read_line()

    def configure(self, name_column_name, category_column_name):
        '''
        Set the configuration parameters.
        '''
        self.category_column_name = category_column_name
        self.name_column_name = name_column_name

    def filename(self):
        '''
        Return the file name and path given in the constructor.
        '''
        return self.filename

    def column_names(self):
        '''
        Return a list of all the column names.
        '''
        return self._current_item.keys()

    def next(self):
        '''
        Return the next item of the archive. An item is a dictionary of
        column name: values. Some values may be lists if they have multiple lines.
        The value for category column is always a list.
        '''
        if not self.category_column_name or not self.name_column_name:
            raise ValueError(_(u'Debes configurar el archivo antes de empezar a leer'))

        # If we reach a completely empty line, finish.
        if not any(self._current_item.values()):
            raise StopIteration()

        item = self._current_item
        self._read_line()

        # Read additional lines with multi values, if any, and convert values to lists.
        while not self._current_item[self.name_column_name]:
            columns_multi = [(name, value) for name, value in self._current_item.items() if value]
            if not columns_multi:
                break
            for name, value in columns_multi:
                if not isinstance(item[name], list):
                    item[name] = [item[name]]
                item[name].append(value)
            try:
                self._read_line()
            except StopIteration:
                break # if end of file is reached, still return the current item.

        # Category column is always a list.
        if not isinstance(item[self.category_column_name], list):
            item[self.category_column_name] = [item[self.category_column_name]]

        return item

    def current_pos(self):
        return self._index - 1

    def _read_line(self):
        try:
            self._current_item = self.reader.next()
            self._index += 1
            for key in self._current_item.keys():
                value = self._current_item[key]
                if type(key) == type(''):  # detect an ASCII key and convert to unicode
                    del self._current_item[key]
                    key = key.decode('utf-8')
                if type(value) == type(''):  # detect an ASCII string and convert to unicode
                    value = value.decode('utf-8')
                if value:
                    value = value.strip()
                self._current_item[key] = value
        except StopIteration:
            #self.csv_file.close()
            raise

