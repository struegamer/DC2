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

import re
import subprocess


class IPMI(object):
    _IPMI_TOOL = '/usr/bin/ipmitool'

    def __init__(self):
        self._ipmi_mac = self._get_ipmi_mac(self._get_ipmitool_output())

    def _get_ipmitool_output(self):
        ipmi_output = None
        try:
            ipmi_output = subprocess.check_output(
                [self._IPMI_TOOL, 'lan', 'print'])
        except subprocess.CalledProcesserror:
            return None
        return ipmi_output

    def _get_ipmi_mac(self, lines):
        _ipmi_mac_re = re.compile('^MAC.*:\s(.*)', re.IGNORECASE | re.X)
        if lines is not None:
            lines = lines.split('\n')
            for line in lines:
                found = _ipmi_mac_re.match(line)
                if found is not None and len(found.groups()) == 1:
                    return found.group(1)
        return None

    def _ipmi_mac(self):
        return self._ipmi_mac

    ipmi_mac = property(_ipmi_mac)
