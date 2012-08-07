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
        column name: values.
        '''
        if not self.category_column_name or not self.name_column_name:
            raise ValueError(_(u'Debes configurar el archivo antes de empezar a leer'))

        if not self._current_item[self.name_column_name] and \
           not self._current_item[self.category_column_name]:
            raise StopIteration()

        item = self._current_item
        self._read_line()

        # Convert the category in the item to a list of categories.
        item[self.category_column_name] = [item[self.category_column_name],]

        # Read additional categories, if any.
        while not self._current_item[self.name_column_name] and \
                  self._current_item[self.category_column_name]:
            item[self.category_column_name].append(self._current_item[self.category_column_name])
            try:
                self._read_line()
            except StopIteration:
                break # if end of file is reached, still return the current item.

        return item

    def _read_line(self):
        try:
            self._current_item = self.reader.next()
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

