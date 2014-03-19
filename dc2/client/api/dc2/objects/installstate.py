# -*- coding: utf-8 -*-
#
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
#

import xmlrpclib

from servers import Servers
from hosts import Hosts


class InstallState(object):

    def __init__(self, rpcurl=None):
        self._rpcurl = rpcurl
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)

    def _update_status(
        self,
        installstate_record=None,
        status=None,
            progress=None):
        if installstate_record is not None:
            if status is not None:
                installstate_record["status"] = status
            if progress is not None:
                installstate_record["progress"] = progress
            if status is not None or progress is not None:
                self._proxy.dc2.deployment.installstate.update(
                    installstate_record)
            return True
        return False

    def find_status_by_server(self, serial_no=None):
        if serial_no is not None and serial_no != "":
            s = Servers(self._rpcurl)
            server_rec = s.find_by_serial_no(serial_no)
            if server_rec is not None:
                installstate = self._proxy.dc2.deployment.installstate.get(
                    {"server_id": server_rec["_id"]})
                if installstate is not None:
                    return installstate
        return None

    def find_status_by_host(self, hostname=None, domainname=None):
        if (hostname is not None and
            hostname != "" and
            domainname is not None and
                domainname != ""):
            h = Hosts(self._rpcurl)
            host_rec = h.find_by_hostname(hostname, domainname)
            if host_rec is not None:
                installstate = self._proxy.dc2.deployment.installstate.get(
                    {"host_id": host_rec["_id"]})
                if installstate is not None:
                    return installstate
        return None

    def update_status_by_server(
        self,
        serial_no=None,
        status=None,
            progress=None):
        if serial_no is not None and serial_no != "":
            s = Servers(self._rpcurl)
            server_rec = s.find_by_serial_no(serial_no)
            if server_rec is not None:
                installstate = self._proxy.dc2.deployment.installstate.get(
                    {"server_id": server_rec["_id"]})
                if installstate is not None:
                    result = self._update_status(
                        installstate, status, progress)
                    return result
        return None

    def update_status_by_host(
        self,
        hostname=None,
        domainname=None,
        status=None,
            progress=None):
        if (hostname is not None and
            hostname != "" and
            domainname is not None and
                domainname != ""):
            h = Hosts(self._rpcurl)
            host_rec = h.find_by_hostname(hostname, domainname)
            if host_rec is not None:
                installstate = self._proxy.dc2.deployment.installstate.get(
                    {"host_id": host_rec["_id"]})
                if installstate is not None:
                    result = self._update_status(
                        installstate, status, progress)
                    return result
        return None
