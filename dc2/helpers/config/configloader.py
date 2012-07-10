# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>
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

import sys
import os
import os.path

try:
    import yaml
except ImportError,e:
    print e
    sys.exit(e)

def read_yaml_file(filename=None,check_config=None):
    if filename is None or filename=='':
        raise IOError('No filename given')
    if not os.path.exists(filename):
        raise IOError('File not found')
    fp=open(filename,'rb')
    yaml_file=fp.read()
    fp.close()
    config_space=yaml.load(yaml_file)
    if check_config is not None:
        if check_config(config_space,filename):
            return config_space
    return None
    
