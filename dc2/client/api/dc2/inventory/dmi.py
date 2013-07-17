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

import os
import sys

class DMI( object ):
    _SYSFS = "/sys/class/dmi/id/"
    _fields = {"manufacturer":_SYSFS + "sys_vendor",
            "serial_no":_SYSFS + "product_serial",
            "uuid":_SYSFS + "product_uuid",
            "asset_tag":_SYSFS + "chassis_asset_tag",
            "product":_SYSFS + "product_name"
            }

    def __init__( self ):
        if self._check_sysfs():
            self._get_fields()
    def _check_sysfs( self ):
        if os.path.exists( "/sys" ):
            if os.path.exists( self._SYSFS ):
                return True
        return False

    def _get_fields( self ):
        for i in self._fields.keys():
            self.__dict__[i] = self._read_value( i )

    def _read_value( self, key ):
        if os.path.exists( self._fields[key] ):
            fp = open( self._fields[key], "rb" )
            value = fp.readline()
            fp.close()
            return value[:-1]
        else:
            return None
