# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

import xmlrpclib
from macs import MACs

class Utilities(object):
    def __init__(self,rpcurl=None):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(self._rpcurl,allow_none=True)

    def get_udev_rule_file_by_mac(self,mac=None):
        if mac is not None and mac != "":
            m=MACs(self._rpcurl)
            mac_rec=m.find(mac)
            if mac_rec is not None:
                udev_file=self._proxy.dc2.deployment.utils.udev.persistent_net_rules({"_id":mac_rec["server_id"]})
                print udev_file
                return udev_file
        return None





