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

import json

from . import SUBPARSERS
from . import _output

from dc2.client.api.dc2.objects import DHCPMgmt


def create_subparser():
    dhcp_parser = SUBPARSERS.add_parser(
        'dhcp',
        description='DHCP Functions',
        help='DHCP Functions')

    dhcp_parser.add_argument(
        '--find-network',
        action='store_true',
        dest='dhcp_find_network',
        default=True,
        help='Find Network')

    dhcp_parser.add_argument(
        'dhcp_ip',
        nargs='?',
        default=None,
        help="IP Address")

    dhcp_parser.set_defaults(
        func=process_dhcp_mgmt,
        parser_name="dhcp")


def process_dhcp_mgmt(args):
    result = False
    if args.dhcp_ip is not None:
        if args.dhcp_find_network:
            dhcp = DHCPMgmt(args.dc2_backend_url)
            network = dhcp.find_entry_by_ip(args.dhcp_ip)
            result = True
            _output(True, json.dumps(network))
    return result
