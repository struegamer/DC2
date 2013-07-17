# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>
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
#################################################################################


import sys
import types

class RecordBase(object):
    def __init__(self, raw_data=None):
        self._raw_data = raw_data

    def __getattr__(self, name):
        if name not in self.__dict__:
            if name in self._raw_data:
                data = self._return_special_data(name)
                if data is not None:
                    return data
                return self._raw_data[name]
            return None
        return self.__dict__[name]

    def _return_special_data(self, name):
        return None

    @property
    def to_dict(self):
        a = {}
        for key in self._raw_data.keys():
            a[key] = eval('self.{0}'.format(key))
        return a
