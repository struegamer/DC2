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


class LSHWProcessors(LSHWBase):
    _NODE_CLASS_NAME = 'processor'

    def __init__(self):
        super(LSHWProcessors, self).__init__()

    def _find_data(self):
        find_cpus = etree.XPath(".//node[@class='{0}]".format(
            self._NODE_CLASS_NAME))

        for cpu in find_cpus(self._inventory):
            _cpus = {}
            for cpu_tag in cpu:
                if cpu_tag.tag == 'configuration':
                    _cpus['configuration'] = {}
                    for config in cpu_tag:
                        config_settings = config.attrib
                        _cpus['configuration'][self._adjust_keys(
                            config_settings['id'])] =\
                            config_settings['value']
                elif cpu_tag.tag == 'capabilities':
                    _cpus['capabilities'] = {}
                    for cap in cpu_tag:
                        cap_data = cap.attrib
                        _cpus['capabilities'][self._adjust_keys(
                            cap_data['id'])] = cap.text
                elif cpu_tag.tag == 'resources':
                    _cpus['resources'] = {}
                    for resource in cpu_tag:
                        resource_data = resource.attrib
                        _cpus['resources'][self._adjust_keys(
                            resource_data['id'])] =\
                            resource_data['value']
                else:
                    _cpus[cpu_tag.tag] = cpu_tag.text
            self._data.append(_cpus)
