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
    from dc2.client.api.dc2 import Environments
except ImportError as e:
    print('{0}: {1}'.format(__file__, e))
    sys.exit(1)


def create_subparser():
    envi_parser = SUBPARSERS.add_parser(
        'environment',
        description='DC2 Environment Functions',
        help='DC2 Environment Functions')

    envi_parser.add_argument(
        '--env',
        action='store',
        dest='env_name',
        default='INVENTORY',
        help='Set Environment Name')

    envi_parser.add_argument(
        'env_variable',
        action='store',
        default=None,
        help='Environment Variable to find')

    envi_parser.set_defaults(
        func=process_environment,
        parser_name="environment")


def process_environment(args):
    result = False
    if args.env_variable is not None and args.env_name is not None:
        env_proxy = Environments(args.dc2_backend_url)
        env_variable = env_proxy.get_environment_variable(
            args.env_name, args.env_variable)
        if env_variable is not None:
            result = True
            _output(result, env_variable)
        else:
            result = False
            _output(
                result,
                'Environment or Environment Variable was not found')
    return result

create_subparser()
