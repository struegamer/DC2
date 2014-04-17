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
import xmlrpclib

try:
    import jinja2
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from dc2.lib.db.mongo import Table
    from dc2.appserver.helpers import check_record
    from dc2.appserver.rpc import rpcmethod
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    import netaddr
except ImportError:
    print "You need to have the python-netaddr module installed"
    sys.exit(1)

try:
    from settings import MONGOS
    from settings import EXT_CONFIG
except ImportError as e:
    print(e)
    sys.exit(1)

tbl_dhcp_mgmt = Table(MONGOS['dc2db']['database'].get_table('dhcp_mgmt'))

DHCP_RECORD = {
    'dcname': True,
    'cluster_no': True,
    'rack_no': True,
    'ipspace': True
}

if 'dhcpd' in EXT_CONFIG:
    DHCP_MGMT_CONFIG = EXT_CONFIG['dhcpd']
else:
    DHCP_MGMT_CONFIG = {}
    DHCP_MGMT_CONFIG['template_file'] = None
    DHCP_MGMT_CONFIG['store_directory'] = '/tmp/'
    DHCP_MGMT_CONFIG['template'] =\
    """subnet {{ip.network}} netmask {{ip.netmask}} {
    range {{ip.range_start}} {{ip.range_end}};
}""" # noqa
    DHCP_MGMT_CONFIG['range_start'] = 100
    DHCP_MGMT_CONFIG['range_end'] = 150


def dc2_dhcp_mgmt_write_config(ipspace=None):
    if ipspace is not None:
        try:
            ip = netaddr.IPNetwork(ipspace)
            if ip.size == 256:
                if DHCP_MGMT_CONFIG['template_file'] is not None:
                    template_env = jinja2.Environment(
                        loader=jinja2.FileSystemLoader(
                            DHCP_MGMT_CONFIG['template_file']))
                    data = {}
                    data['ip'] = {}
                    data['ip']['network'] = str(ip.network)
                    data['ip']['netmask'] = str(ip.netmask)
                    data['ip']['range_start'] = ip[DHCP_MGMT_CONFIG[
                        'range_start']]
                    data['ip']['range_end'] = ip[DHCP_MGMT_CONFIG[
                        'range_end']]

        except netaddr.core.AddrFormatError as e:
            pass
