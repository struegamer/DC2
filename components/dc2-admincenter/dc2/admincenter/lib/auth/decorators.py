# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
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
    import web
except ImportError:
    print("You don't have web.py installed")
    sys.exit(1)


def needs_auth(func):
    def wrapper(*args, **kwargs):
        if 'session' in web.ctx:
            if 'authenticated' in web.ctx.session:
                if web.ctx.session.authenticated is True:
                    return func(*args, **kwargs)
        raise web.HTTPError(
            '400 Bad Request',
            {'Content-Type': 'text/html; charset=utf-8'},
            """You are not authenticated!""")
    return wrapper


def needs_admin(func):
    def wrapper(*args, **kwargs):
        if 'session' in web.ctx:
            if 'is_dc2admin' in web.ctx.session:
                if web.ctx.session.is_dc2admin is True:
                    return func(*args, **kwargs)
        raise web.HTTPError(
            '400 Bad Request',
            {'Content-Type': 'text/html; charset=utf-8'},
            """You are not authenticated!""")
    return wrapper
