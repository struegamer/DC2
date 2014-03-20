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
    from dc2.client.api.dc2.cliparsers import PARSER
except ImportError as e:
    print(e)
    sys.exit(1)


def main():
    create_argparser()
    args = PARSER.parse_args()
    result = args.func(args)
    if result is False:
        return(-2)


def create_argparser():
    PARSER.add_argument(
        '--dc2-backend-url',
        action='store',
        dest="dc2_backend_url",
        metavar='<url to your DC2 backend server>',
        help="DC2 Backend URL",
        default=None,
        required=True,
    )
