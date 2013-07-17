# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>
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
#################################################################################
__all__ = ['connectionpool']

import sys
try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)

try:
    from dc2.lib.db.mongo import ConnectionPool
    from dc2.lib.db.mongo import Database
except ImportError:
    print "you don't have DC² correctly installed"
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError:
    print "You don't have a settings file"
    sys.exit(1)

connectionpool = ConnectionPool()
for conn in MONGOS.keys():
    connectionpool.connect(MONGOS[conn]["dbname"], MONGOS[conn]["host"], MONGOS[conn]["port"])
    MONGOS[conn]["database"] = Database(connectionpool.get_connection(), MONGOS[conn]["dbname"])


