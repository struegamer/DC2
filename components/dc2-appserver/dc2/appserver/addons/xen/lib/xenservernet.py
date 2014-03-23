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

import xmlrpclib
from helper import parse_output


def xenserver_network_list(xenhost=None, session_id=None):
    if xenhost is not None and session_id is not None:
        s = xmlrpclib.ServerProxy(
            "https://{0}/".format(xenhost),
            allow_none=True)
        network_names = []
        network_list = parse_output(s.network.get_all(session_id))
        if network_list:
            for network in network_list:
                d = parse_output(s.network.get_record(session_id, network))
                d["network_id"] = network
                d["xen_host"] = xenhost
                d["session_id"] = session_id
                network_names.append(d)
            return network_names
    return None


def xenserver_network_get_record(
    xenhost=None,
    session_id=None,
        network_id=None):
    if (xenhost is not None and
            session_id is not None and
            network_id is not None and
            xenhost != "" and
            session_id != "" and
            network_id != ""):
        s = xmlrpclib.ServerProx(
            "https://{0}/".format(xenhost),
            allow_none=True)
        d = parse_output(s.network.get_record(session_id, network_id))
        d["network_id"] = network_id
        d["xen_host"] = xenhost
        d["session_id"] = session_id
        return d
    return None
