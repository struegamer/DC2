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

import sys

try:
    from lxml import etree
except ImportError as e:
    print('No lxml installed')
    print(e)
    sys.exit(1)

from .lshw_base import LSHWBase


class LSHWDisks(LSHWBase):
    _NODE_CLASS_NAME = 'disk'

    def __init__(self):
        super(LSHWDisks, self).__init__()

    def _find_data(self):
        find_disks = etree.XPath(".//[@class='{0}']".format(
            self._NODE_CLASS_NAME))

        for disk in find_disks(self._inventory):
            _disks = {}
            for disk_tag in disk:
                if disk_tag.tag == 'configuration':
                    _disks['configuration'] = {}
                    for config in disk_tag:
                        config_settings = config.attrib
                        _disks['configuration'][config_settings['id']] =\
                            config_settings['value']
                elif disk_tag.tag == 'capabilities':
                    _disks['capabilities'] = {}
                    for cap in disk_tag:
                        cap_data = cap.attrib
                        _disks['capabilities'][cap_data['id']] = cap.text
                elif disk_tag.tag == 'resources':
                    _disks['resources'] = {}
                    for resource in disk_tag:
                        resource_data = resource.attrib
                        _disks['resources'][resource_data['type']] =\
                            resource_data['value']
                else:
                    _disks[disk_tag.tag] = disk_tag.text
            self._data.append(_disks)
