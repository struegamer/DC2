# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#


class MemoryInfo(object):
    _MEMINFO = '/proc/meminfo'

    def __init__(self):
        self._meminfo = {}
        self._read_meminfo()

    def _read_meminfo(self):
        fp = open('/proc/meminfo', 'rb')
        for line in fp:
            a = line.split(':')
            b = {}
            b[a[0].strip()] = a[1].strip()
            self._meminfo.update(b)
        fp.close()

    def meminfo(self):
        return self._meminfo
