# -*- coding: utf-8 -*-
#
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import subprocess

try:
    from lxml import etree
except ImportError:
    print('You didn\'t install lxml')
    sys.exit(1)


class LSHWBase(object):
    _LSHW_BIN = '/usr/bin/lshw'

    def __init__(self):
        self._inventory = None
        self._data = []
        self._get_lshw_data()
        self._find_data()

    def _get_lshw_data(self):
        lshw_output = subprocess.check_output([self._LSHW_BIN, '-xml'])
        self._inventory = etree.XML(lshw_output.decode('utf-8'))

    def _find_data(self):
        pass

    def _get_data(self):
        return self._data
    data = property(_get_data)
