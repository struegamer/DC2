# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################

#
# Std. Python Libs
#
import sys
import types
import re
import uuid

try:
    from dc2.lib.db.mongo import Database
    from dc2.lib.db.mongo import Table
except ImportError as e:
    print('You don not have dc2.lib installed')
    print(e)
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError as e:
    print('You do not have a settings file')
    print(e)
    sys.exit(1)

tbl_users = Table(MONGOS['admincenter']['database'].get_table("users"))


def users_list():
    result = tbl_users.find()
    if result is not None:
        return result
    return []


def users_new():
    rec = {}
    rec['username'] = ''
    rec['password'] = ''
    rec['fullname'] = ''
    return rec


def users_add(rec=None):
    pass


def users_update(rec=None):
    pass


def users_get(rec=None):
    pass


def users_delete(rec=None):
    pass
