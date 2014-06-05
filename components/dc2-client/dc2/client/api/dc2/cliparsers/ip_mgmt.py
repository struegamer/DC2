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
from socket import inet_aton
import struct

from . import SUBPARSERS
from . import _output

# from dc2.client.api.dc2.objects import DHCPMgmt
try:
    import netifaces
except ImportError as e:
    print('{0}: {1}'.format(__file__, e))
    sys.exit(1)


def create_subparser():
    ip_parser = SUBPARSERS.add_parser(
        'ip',
        description="IP Management Functions",
        help="IP Management Functions")

    ip_parser.add_argument(
        '--get-ip',
        action='store_true',
        dest='ip_get_ip',
        default=False,
        help='Get IP')

    ip_parser.add_argument(
        'ip_device_name',
        default='lo',
        help="Device Name")

    ip_parser.set_defaults(
        func=process_ip,
        parser_name='ip')


def process_ip(args):
    result = False
    if args.ip_get_ip:
        if args.ip_device_name:
            if args.ip_device_name in netifaces.interfaces():
                result = True
                addrs = netifaces.ifaddresses(args.ip_device_name)
                for i in addrs:
                    if 'addr' not in i:
                        result = False
                        break
                if result:
                    addrs_sorted = sorted(
                        addrs[netifaces.AF_INET],
                        key=lambda ip: struct.unpack(
                            '!L', inet_aton(ip['addr']))[0])
                    for i in addrs_sorted:
                        _output(result, i['addr'])
            else:
                result = False
                _output(False, 'Network Interface {0} does not exist'.format(
                    args.ip_device_name))
    return False

create_subparser()
