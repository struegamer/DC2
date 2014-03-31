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


class LSHWStorage(LSHWBase):
    _NODE_CLASS_NAME = 'storage'

    def __init__(self):
        super(LSHWStorage, self).__init__()

    def _find_data(self):
        find_storage = etree.XPath(".//node[@class='{0}']".format(
            self._NODE_CLASS_NAME))

        for storage_bus in find_storage(self._inventory):
            _storages = {}
            for storage_tag in storage_bus:
                if storage_tag.tag == 'configuratrion':
                    _storages['configuration'] = {}
                    for config in storage_tag:
                        config_settings = config.attrib
                        _storages['configuration'][config_settings['id']] =\
                            config_settings['value']
                elif storage_tag.tag == 'capabilities':
                    _storages['capabilities'] = {}
                    for cap in storage_tag:
                        cap_data = cap.attrib
                        _storages['capabilities'][cap_data['id']] = cap.text
                elif storage_tag.tag == 'resources':
                    _storages['resources'] = {}
                    for resource in storage_tag:
                        resource_data = resource.attrib
                        _storages['resources'][resource_data['type']] =\
                            resource_data['value']
                else:
                    _storages[storage_tag.tag] = storage_tag.text
            self._data.append(_storages)
