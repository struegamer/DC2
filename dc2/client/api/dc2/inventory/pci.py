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

import subprocess
import re
import os
import os.path

class PCIDevices(object):
    LSPCI="/usr/bin/lspci"

    def __init__(self):
        if not os.path.exists(self.LSPCI):
            raise FileNotFoundException("%s not found" % LSPCI)
        self._read_lspci_output()
        self._parse_lspci_output()
    def _read_lspci_output(self):
        p=subprocess.Popen([self.LSPCI,"-vmm"],stdout=subprocess.PIPE)
        (self._stdoutdata,self._stderrdata)=p.communicate()
    def _parse_lspci_output(self):
        c1=re.compile(r"(.*?)\n\n",re.MULTILINE|re.S)
        findlist=c1.findall(self._stdoutdata)
        c2=re.compile(r"(.*?)\s+:\s+(.*)")
        self._device_list=[]
        for entry in findlist:
            dev_hash={}
            entry_split=entry.split("\n")
            for line in entry_split:
                (key,value)=line.split(":\t")
                dev_hash[key.lower()]=value
            self._device_list.append(dev_hash)

    def get_pci_devices(self):
        return self._device_list


