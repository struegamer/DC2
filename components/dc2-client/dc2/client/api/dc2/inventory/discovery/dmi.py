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

import os


class DMI(object):
    _SYSFS = "/sys/class/dmi/id"
    _fields = {
        "manufacturer": '{0}/{1}'.format(_SYSFS, "sys_vendor"),
        "serial_no": '{0}/{1}'.format(_SYSFS, "product_serial"),
        "uuid": '{0}/{1}'.format(_SYSFS, "product_uuid"),
        "asset_tag": '{0}/{1}'.format(_SYSFS, "chassis_asset_tag"),
        "product": '{0}/{1}'.format(_SYSFS, "product_name"),
        "bios_date": '{0}/{1}'.format(_SYSFS, "bios_date"),
        "bios_vendor": '{0}/{1}'.format(_SYSFS, "bios_vendor"),
        "bios_version": '{0}/{1}'.format(_SYSFS, "bios_version"),
        "board_name": '{0}/{1}'.format(_SYSFS, "board_name"),
        "board_serial": '{0}/{1}'.format(_SYSFS, "board_serial"),
        "board_vendor": '{0}/{1}'.format(_SYSFS, "board_vendor"),
        "board_version": '{0}/{1}'.format(_SYSFS, "board_version")
    }

    def __init__(self):
        if self._check_sysfs():
            self._get_fields()

    def _check_sysfs(self):
        if os.path.exists("/sys"):
            if os.path.exists(self._SYSFS):
                return True
        return False

    def _get_fields(self):
        for i in self._fields.keys():
            self.__dict__[i] = self._read_value(i)

    def _read_value(self, key):
        if os.path.exists(self._fields[key]):
            fp = open(self._fields[key], "rb")
            value = fp.readline()
            fp.close()
            return value[:-1]
        else:
            return None
