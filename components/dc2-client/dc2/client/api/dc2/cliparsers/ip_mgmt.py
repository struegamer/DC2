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

# from dc2.client.api.dc2.objects import DHCPMgmt


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
        parser_nmae='ip')


def process_ip(args):
    pass
