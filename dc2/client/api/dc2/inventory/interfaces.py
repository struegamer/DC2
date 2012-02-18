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

import re
import subprocess

class Interfaces(object):
    def __init__(self):
        self._get_nics()
    def _get_nics(self):
        ipconfig=subprocess.Popen(["ip","l"],stdout=subprocess.PIPE)
        p=re.compile(r"\s+link/ether\s+([a-zA-Z0-9:]+)", re.VERBOSE)
        self.__dict__["nics"]=[]
        for i in ipconfig.stdout:
            found=p.search(i)
            if found is not None:
                self.__dict__["nics"].append(found.group(1))
