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

from . import SUBPARSERS
from . import _output

try:
    from dc2.web.client import DC2SocketClient
    from dc2.web.client import Commands
except ImportError as e:
    print(e)
    sys.exit(1)


def create_subparsers():
    state_parser = SUBPARSERS.add_parser(
        'state',
        description="Adjust the state for discovery/deployment",
        help='State related functions'
    )

    state_group = state_parser.add_mutually_exclusive_group(required=True)

    state_group.add_argument(
        '--event',
        action='store_true',
        default=False,
        dest='state_event',
        help='State change will be pushed through socketIO')

    state_group.add_argument(
        '--deployment-state',
        action='store_true',
        default=True,
        dest='state_deployment_state',
        help='deployment state'
    )

    state_parser.add_argument(
        '--deploment-status',
        action='store',
        dest="state_deployment_status",
        choices=[],
        help='Choice of Deployment States')

    state_parser.add_argument(
        '--event-code',
        action='store',
        dest='state_event_code',
        choices=[],
        help='Choice of Event Codes')

    state_parser.set_default(
        func=process_state,
        parser_name='state'
    )


def process_state(args):
    result=False
    return result
