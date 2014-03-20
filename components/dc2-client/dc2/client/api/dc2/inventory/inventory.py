# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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
###############################################################################

import xmlrpclib

from dmi import DMI
from interfaces import Interfaces
from pci import PCIDevices
from cpu import CPUInfo
from meminfo import MemoryInfo


class ServerInventory(object):
    def __init__(self, rpcurl):
        self._rpcurl = rpcurl
        self._dmi = DMI()
        self._nics = Interfaces()
        self._pcidevices = PCIDevices()
        self._meminfo = MemoryInfo()
        self._cpuinfo = CPUInfo()
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)

    def _add_server(self):
        server_rec = {}
        server_rec["uuid"] = self._dmi.uuid
        #
        # Check if serial number is empty or 0 or None
        # If so, add some String and the uuid to it.
        # Faking Serial numbers
        #

        if (self._dmi.serial_no == "0" or
                self._dmi.serial_no == "" or
                self._dmi.serial_no is None):
            server_rec["serial_no"] = "Serial_{0}".format(self._dmi.uuid)
        else:
            server_rec["serial_no"] = self._dmi.serial_no
        server_rec["product_name"] = self._dmi.product
        server_rec["manufacturer"] = self._dmi.manufacturer
        server_rec["location"] = "New Server"
        server_rec["asset_tags"] = "New Asset"
        server_rec["pci_devices"] = self._pcidevices.get_pci_devices()
        server_rec["cpuinfo"] = self._cpuinfo.processors()
        server_rec['cpucount'] = self._cpuinfo.num_of_processors()
        server_rec['memoryinfo'] = self._meminfo.meminfo()
        server_doc_id = self._proxy.dc2.inventory.servers.add(server_rec)
        if server_doc_id is not None:
            counter = 0
            for i in self._nics.nics:
                nic_rec = {}
                nic_rec["server_id"] = server_doc_id
                nic_rec["mac_addr"] = i
                nic_rec["device_name"] = "eth{0}".format(counter)
                self._proxy.dc2.inventory.servers.macaddr.add(nic_rec)
                counter = counter + 1
            host_rec = {}
            host_rec["server_id"] = server_doc_id
            host_rec["hostname"] = server_rec["serial_no"]
            host_rec["domainname"] = "INVENTORY"
            host_rec["hostclasses"] = []
            host_rec["environments"] = "INVENTORY"
            host_doc_id = self._proxy.dc2.inventory.hosts.add(host_rec)
            install_rec = {}
            install_rec["server_id"] = server_doc_id
            install_rec["host_id"] = host_doc_id
            install_rec["status"] = "localboot"
            install_rec["progress"] = "None"
            install_rec["hostname"] = "{0}.{1}".format(
                server_rec["serial_no"], "INVENTORY")
            self._proxy.dc2.deployment.installstate.add(install_rec)

    def doInventory(self):
        self._add_server()
