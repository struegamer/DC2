# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

import os


class CPUInfo(object):
    _CPUINFO = '/proc/cpuinfo'

    def __init__(self):
        self._processors = []
        self._read_cpuinfo()

    def _read_cpuinfo(self):
        if os.path.exists(self._CPUINFO):
            fp = open(self._CPUINFO, 'rb')
            processor = {}
            for line in fp:
                if len(processor)<=0:
                    processor = {}
                a = line.split(":")
                if len(a) != 1:
                    key = a[0].strip()
                    value = a[1].strip()
                    if key == 'processor':
                        processor = {}
                    processor[key] = value
                else:
                    self._processors.append(processor)
            fp.close()

    def num_of_processors(self):
        return len(self._processors)

    def processors(self):
        return self._processors
