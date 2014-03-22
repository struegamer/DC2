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

from .lshw_base import LSHWBase


class LSHWGenerics(LSHWBase):
    _NODE_CLASS_NAME = 'generic'

    def __init__(self):
        super(LSHWGenerics, self).__init__()
        self._data = []
        self._find_data()

    def _find_data(self):
        find_generics = etree.XPath(".//node[@class='{0}']".format(
            self._NODE_CLASS_NAME))
        for generic in find_generics(self._inventory):
            _generics = {}
            for generic_tag in generic:
                if generic_tag.tag == 'configuration':
                    _generics['configuration'] = {}
                    for config in generic_tag:
                        config_settings = config.attrib
                        _generics['configuration'][config_settings['id']] =\
                            config_settings['value']
                elif generic_tag.tag == 'capabilities':
                    _generics['capabilities'] = {}
                    for cap in generic_tag:
                        cap_data = cap.attrib
                        _generics['capabilities'][cap_data['id']] = cap.text
                elif generic_tag.tag == 'resources':
                    _generics['resources'] = {}
                    for resource in generic_tag:
                        resource_data = resource.attrib
                        _generics['resources'][resource_data['type']] =\
                            resource_data['value']
                else:
                    _generics[generic_tag.tag] = generic_tag.text
            self._data.append(_generics)

    def _get_data(self):
        return self._data
    data = property(_get_data)
