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
import json

from . import SUBPARSERS
from . import _output

try:
    from dc2.web.client import DC2SocketClient
    from dc2.web.client import Commands
    from dc2.web.client import EVENTS
except ImportError as e:
    print(__file__)
    print(e)
    sys.exit(1)


def create_subparsers():
    state_parser = SUBPARSERS.add_parser(
        'events',
        description="Events",
        help='Event related functions'
    )

    state_parser.add_argument(
        '--event-host',
        action='store',
        dest='event_host',
        default=None,
        help='Event WebApp hostname',
        required=True
    )
    state_parser.add_argument(
        '--event-port',
        action='store',
        dest='event_port',
        default=80,
        type=int,
        help='Event WebApp Port',
        required=True)

    state_parser.add_argument(
        '--event-code',
        action='store',
        dest='event_code',
        choices=[event for event in EVENTS.keys()],
        default=None,
        required=True,
        help='Choice of Event Codes')

    state_parser.add_argument(
        'event_json_data',
        nargs='?',
        default=None,
        help='Event JSON data as string'
    )

    state_parser.set_defaults(
        func=process_state,
        parser_name='state'
    )


def process_state(args):
    result = False
    if args.event_host is not None and args.event_port != 0:
        dc2_socket_client = DC2SocketClient(
            host=args.event_host,
            port=args.event_port)
        commands = Commands(dc2_socket_client)
        if args.event_code is not None:
            if args.event_json_data is not None:
                print(type(args.event_json_data))
                try:
                    print(args.event_json_data)
                    commands.send_event(
                        args.event_code,
                        json.loads(
                            args.event_json_data),
                        wait=2)
                    result = True
                except Exception as e:
                    print(json.loads(args.event_json_data))
                    _output(False, '{0}: {1}'.format(__file__, e))
                    result = False
    return result

create_subparsers()
