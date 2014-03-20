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
import re
import json

from . import SUBPARSERS
from . import _output

try:
    from dc2.client.api.dc2 import Hosts
except ImportError as e:
    print(e)
    sys.exit(1)


def create_subparser():
    host_parser = SUBPARSERS.add_parser(
        'hosts',
        description='Host related functions', help='Host related functions')
    host_parser_search_group = host_parser.add_mutually_exclusive_group()
    host_parser_search_group.add_argument(
        '--find-mac',
        action='store_true',
        dest='find_mac',
        default=False,
        help='Find host by mac address'
    )
    host_parser_search_group.add_argument(
        '--find-serial-no',
        action='store_true',
        default=False,
        help='Find host by serial no'
    )
    host_parser_search_group.add_argument(
        '--find-fqdn',
        action="store_true",
        default=False,
        help='Find host by FQDN'
    )
    host_parser.add_argument(
        '--output-value',
        action="store",
        dest='output_value',
        metavar='<hostname|domainname|environments|server_id|fqdn|all>',
        choices=[
            'hostname',
            'domainname',
            'environments',
            'server_id',
            'fqdn',
            'all'
        ],
        required=True
    )
    host_parser.add_argument(
        'value',
        action='store',
        help='The search value'
    )

    host_parser.set_defaults(func=process_hosts, parser_name="hosts")


def process_hosts(args):
    result = False
    host_rpc = Hosts(args.dc2_backend_url)
    if args.find_mac is True:
        message, result = _find_host_by_mac(
            host_rpc,
            args.value,
            args.output_value
        )
    if args.find_serial_no is True:
        message, result = _find_host_by_serial(
            host_rpc,
            args.value,
            args.output_value
        )
    if args.find_fqdn is True:
        message, result = _find_host_by_fqdn(
            host_rpc,
            args.value,
            args.output_value
        )
    _output(result, message)
    return result


def _find_host_by_mac(host_rpc, mac, output_value):
    mac_addr_re = re.compile(r'([0-9A-F]{2}[:]){5}([0-9A-F]{2})', re.I)
    check_mac = mac_addr_re.match(mac)
    if check_mac is None:
        err_msg = '{0} is not a MAC Address'.format(mac)
        return (err_msg, False)
    try:
        host = host_rpc.find_by_server_mac(mac)
        return _output_host_message(host, output_value)
    except Exception as e:
        print(e)
        sys.exit(1)


def _find_host_by_serial(host_rpc, serial, output_value):
    try:
        host = host_rpc.find_by_server_serial(serial)
        return _output_host_message(host, output_value)
    except Exception as e:
        print(e)
        sys.exit(1)


def _find_host_by_fqdn(host_rpc, fqdn, output_value):
    try:
        hostname = fqdn.split('.', 1)[0]
        domainname = fqdn.split('.', 1)[1]
        host = host_rpc.find_by_hostname(hostname, domainname)
        return _output_host_message(host, output_value)
    except Exception as e:
        print(e)
        sys.exit(1)


def _output_host_message(host, output_value):
    if host is None:
        return ('Host not found', False)
    if output_value == 'all':
        return (json.dumps(host, sort_keys=True, indent=2), True)
    elif output_value == 'fqdn':
        return ('{0}.{1}'.format(host['hostname'], host['domainname']), True)
    elif output_value not in host:
        return ('Output Value not found in host record', False)
    else:
        return (host[output_value], True)

create_subparser()
