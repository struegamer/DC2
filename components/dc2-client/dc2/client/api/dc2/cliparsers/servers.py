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
    from dc2.client.api.dc2 import Servers
except ImportError as e:
    print(e)
    sys.exit(-1)


def create_subparser():
    server_parser = SUBPARSERS.add_parser(
        'servers',
        description='Server related functions',
        help='Server related functions')
    server_parser_search_group = server_parser.add_mutually_exclusive_group()
    server_parser_search_group.add_argument(
        '--find-mac',
        action="store_true",
        dest='find_mac',
        default=False,
        help='Find a server by MAC Address')
    server_parser_search_group.add_argument(
        '--find-uuid',
        action='store_true',
        dest='find_uuid',
        default=False,
        help='Find a server by its UUID'
    )
    server_parser_search_group.add_argument(
        '--find-serial-no',
        action='store_true',
        dest='find_serial_no',
        default=False,
        help='Find a server by its Serial Number'
    )
    server_parser.add_argument(
        '--output-value',
        action='store',
        dest='output_value',
        metavar='<key from server record or all>',
        required=True)
    server_parser.add_argument(
        'value',
        action='store',
        help="The search value"
    )
    server_parser.set_defaults(func=process_server, parser_name='servers')


def process_server(args):

    result = False
    server_rpc = Servers(args.dc2_backend_url)
    if args.find_mac is True:
        message, result = _find_server_by_mac(
            server_rpc,
            args.value,
            args.output_value)
    if args.find_uuid is True:
        message, result = _find_server_by_uuid(
            server_rpc,
            args.value,
            args.output_value)
    if args.find_serial_no is True:
        message, result = _find_server_by_serial_no(
            server_rpc,
            args.value,
            args.output_value
        )
    _output(result, message)
    return result


def _output_server_message(server, output_value):
    if server is None:
        return ('Server not found', False)
    if output_value == 'all':
        return (json.dumps(server, sort_keys=True, indent=2), True)
    elif output_value not in server:
        return('Output Value not found in server record', False)
    else:
        return(server[output_value], True)


def _find_server_by_uuid(server_rpc, uuid_str, output_value):
    try:
        server = server_rpc.find_by_uuid(uuid_str)
        return _output_server_message(server, output_value)
    except Exception as e:
        print(e)
        sys.exit(1)


def _find_server_by_serial_no(server_rpc, serial_no, output_value):
    try:
        server = server_rpc.find_by_serial_no(serial_no)
        return _output_server_message(server, output_value)
    except Exception as e:
        print(e)
        sys.exit(1)


def _find_server_by_mac(server_rpc, mac_addr, output_value):
    mac_addr_re = re.compile(r'([0-9A-F]{2}[:]){5}([0-9A-F]{2})', re.I)
    check_mac = mac_addr_re.match(mac_addr)
    if check_mac is None:
        err_msg = '{0} is not a MAC Address'.format(mac_addr)
        return (err_msg, False)
    try:
        server = server_rpc.find_by_mac(mac_addr)
        return _output_server_message(server, output_value)
    except Exception as e:
        print(e)
        sys.exit(1)

create_subparser()
