# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
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
except ImportError:
    print('You didn\'t install lxml')
    sys.exit(1)

from lshw_base import LSHWBase


class LSHWNics(LSHWBase):
    _NODE_CLASS_NAME = 'network'

    def __init__(self):
        super(LSHWNics, self).__init__()
        self._nics = []
        self._find_nics()

    def _find_nics(self):
        find_nics = etree.XPath(".//node[@class='{0}']".format(
            self._NODE_CLASS_NAME))
        _nics = {}
        for nic in find_nics(self._inventory):
            for nic_tag in nic:
                if nic_tag.tag == 'configuration':
                    _nics['configuration'] = {}
                    for config in nic_tag:
                        config_settings = config.attrib
                        _nics['configuration'][config_settings['id']] =\
                            config_settings['value']
                elif nic_tag.tag == 'capabilities':
                    _nics['capabilities'] = {}
                    for cap in nic_tag:
                        cap_data = cap.attrib
                        _nics['capabilities'][cap_data['id']] = cap.text
                elif nic_tag.tag == 'resources':
                    _nics['resources'] = {}
                    for resource in nic_tag:
                        resource_data = resource.attrib
                        _nics['resources'][resource_data['type']] =\
                            resource_data['value']
                else:
                    _nics[nic_tag.tag] = nic_tag.text

            self._nics.append(_nics)

    def _get_nics(self):
        return self._nics
    nics = property(_get_nics)
