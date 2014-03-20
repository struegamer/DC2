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
import imp

from . import SUBPARSERS
from . import _output  # noqa


def create_subparser():
    discovery_parser = SUBPARSERS.add_parser(
        'discovery',
        description='Discovery related functions',
        help='Discovery related functions'
    )
    discovery_parser.add_argument(
        '--dry-run',
        action='store_true',
        dest='dry_run',
        default=False,
        help='Dry Run, don\'t write anything to the database and output only'
    )
    discovery_parser.add_argument(
        '--use-discovery-module',
        action='store',
        dest='discovery_module',
        default=None,
        metavar='<classname>',
        help='Use special discovery module'
    )

    discovery_parser.set_defaults(
        func=process_discovery,
        parser_name='discovery')


def process_discovery(args):
    result = False
    if args.discovery_module is None:
        try:
            from dc2.client.api.dc2 import ServerInventory
            s = ServerInventory(args.dc2_backend_url)  # noqa
            s.doInventory()
        except Exception as e:
            print(e)
            sys.exit(1)
    else:
        pass
        # from dc2.gaikai.client.inventory import ServerInventory
        # s = ServerInventory(args.dc2_backend_url)
        # s.doInventory()
create_subparser()
