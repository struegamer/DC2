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
import os
import os.path

try:
    import yaml
except ImportError as e:
    print(e)
    sys.exit(e)


class Configuration(object):

    def __init__(self, filename=None, check_config=None):
        if filename is None or filename == '':
            raise IOError('No filename given')
        if not os.path.exists(filename):
            raise IOError('File not found')
        self._configfilename = filename
        self._func_check_config = check_config
        self._read_yaml_file()

    def _read_yaml_file(self):
        fp = open(self._configfilename, 'rb')
        yaml_file = fp.read()
        fp.close()
        self._config_space = yaml.load(yaml_file)
        if self._check_config():
            return True
        return False

    def _check_config(self):
        if self._func_check_config is not None:
            if self._func_check_config(
                    self._config_space,
                    self._configfilename):
                return True
        return False

    def _get_config_space(self):
        return self._config_space

    config_space = property(_get_config_space)
