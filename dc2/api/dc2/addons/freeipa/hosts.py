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

from dc2.api import RPCClient

class Hosts(RPCClient):

    def check(self, fqdn=None):
        if fqdn is None:
            return None
        result = self._proxy.dc2.freeipa.hosts.check(fqdn)
        if result is not None:
            return True
        return False

    def get(self, fqdn=None):
        if fqdn is None:
            return None
        result = self._proxy.dc2.freeipa.hosts.get(fqdn)
        if result is not None:
            return result
        return False

    def add(self, fqdn=None, infos=None):
        if fqdn is None or infos is None:
            return None
        result = self._proxy.dc2.freeipa.hosts.add(fqdn, infos)
        if result is not None:
            return result
        return False
    def delete(self, fqdn=None):
        if fqdn is None or infos is None:
            return None
        result = self._proxy.dc2.freeipa.hosts.delete(fqdn, infos)
        if result is not None:
            return result
        return False

