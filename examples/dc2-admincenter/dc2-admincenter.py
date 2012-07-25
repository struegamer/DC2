# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>
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

import sys
import os
import os.path



abspath = os.path.dirname(__file__)
if abspath is not None and abspath != "":
    sys.path.append(abspath)
    os.chdir(abspath)


try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)


try:
    from dc2.admincenter.globals import connectionpool
    from dc2.lib.db.mongo import MongoStore
except ImportError,e:
    print "Your DC2 installation is not correct"
    print e
    sys.exit(1)
#
# Apps Import
#
try:
    from dc2.admincenter.apps import Home
    from dc2.admincenter.apps import Login
except ImportError,e:
    print "You didn't install DC² correctly"
    print e
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError,e:
    print 'You do not have a settings file.'
    sys.exit(1)

urls = (
    "/", "Home",
    "/login","Login")

session_db=MONGOS["admincenter"]["database"].get_db()

app = web.application(urls, globals(), autoreload=True)
sessions=web.session.Session(app,MongoStore(session_db,'sessions'))


def session_hook():
    web.ctx.session=sessions

app.add_processor(web.loadhook(session_hook))

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
