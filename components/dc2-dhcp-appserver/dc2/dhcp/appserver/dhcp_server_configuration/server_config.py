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

try:
    import jinja2
except ImportError as e:
    print(e)
    sys.exit(1)

# try:
#     from dc2.lib.db.mongo import Table
# except ImportError as e:
#     print(e)
#     sys.exit(1)

try:
    import netaddr
except ImportError:
    print "You need to have the python-netaddr module installed"
    sys.exit(1)

try:
    from settings import EXT_CONFIG
except ImportError as e:
    EXT_CONFIG = {}


# tbl_dhcp_mgmt = Table(MONGOS['dc2db']['database'].get_table('dhcp_mgmt'))

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
    next-server {{ip.next_server}};
    option routers {{ip.option_routers}};
    option domain-name-servers {{ip.option_domain_name_servers}};
    if exists user-class and option user-class = "iPXE" {
        filename "{{ip.dc2db_ipxe_url}}";
    } else {
        filename "undionly.kpxe";
    }
}"""  # noqa
    DHCP_MGMT_CONFIG['range_start'] = 100
    DHCP_MGMT_CONFIG['range_end'] = 150
    DHCP_MGMT_CONFIG['dc2db_ipxe_url'] = 'http://localhost/ipxe'
    DHCP_MGMT_CONFIG['option_domain_name_servers'] = '127.0.0.1'
    DHCP_MGMT_CONFIG['next_server'] = '127.0.0.1'


def dc2_dhcp_mgmt_write_config(ipspace=None):
    template = None
    if ipspace is not None:
        print('hello')
        try:
            ip = netaddr.IPNetwork(ipspace)
            if ip.size == 256:
                if (DHCP_MGMT_CONFIG['template'] is not None and
                        DHCP_MGMT_CONFIG['template_file'] is None):
                    template = jinja2.Template(DHCP_MGMT_CONFIG['template'])
                elif (DHCP_MGMT_CONFIG['template_file'] is not None and
                        DHCP_MGMT_CONFIG['template'] is None):
                    template_env = jinja2.Environment(
                        loader=jinja2.FileSystemLoader(
                            DHCP_MGMT_CONFIG['template_dir']))
                    template = template_env.get_template(
                        DHCP_MGMT_CONFIG['template_file'])
                if template is not None:
                    data = {}
                    data['ip'] = {}
                    data['ip']['network'] = str(ip.network)
                    data['ip']['netmask'] = str(ip.netmask)
                    data['ip']['range_start'] = ip[DHCP_MGMT_CONFIG[
                        'range_start']]
                    data['ip']['range_end'] = ip[DHCP_MGMT_CONFIG[
                        'range_end']]
                    data['ip']['dc2db_ipxe_url'] = DHCP_MGMT_CONFIG[
                        'dc2db_ipxe_url']
                    data['ip']['option_routers'] = ip[1]
                    data['ip']['option_domain_name_servers'] =\
                        DHCP_MGMT_CONFIG['option_domain_name_servers']
                    data['ip']['next_server'] =\
                        DHCP_MGMT_CONFIG['next_server']
                    rendered_template = template.render(data)
                    print(template)
                    fp = open(
                        '{0}/{1}'.format(
                            DHCP_MGMT_CONFIG['store_directory'],
                            '{0}.conf'.format(str(ip.network))),
                        'wb')
                    fp.write(rendered_template)
                    fp.close()
                    dc2_dhcp_mgmt_manage_include_file(
                        'add', '{0}.conf'.format(str(ip.network)))
                    return True
                else:
                    return False
        except netaddr.core.AddrFormatError:
            return False
    else:
        return False


def dc2_dhcp_mgmt_manage_include_file(action='add', filename_to_add=None):
    dhcp_include_file = DHCP_MGMT_CONFIG['dhcp_include_file']
    dhcp_store_directory = DHCP_MGMT_CONFIG['store_directory']

    if action.lower() == 'add':
        fp = open(dhcp_include_file, 'r+b')
        contents = fp.readlines()
        found = False
        for line in contents:
            if line.find('include "{0}{1}";'.format(
                dhcp_store_directory,
                    filename_to_add)) == -1:
                found = False
            else:
                found = True
                break
        if found is False:
            fp.write('include "{0}{1}";'.format(
                dhcp_store_directory, filename_to_add))
        fp.close()
    elif action.lower() == 'delete':
        pass
