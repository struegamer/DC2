# -*- coding: utf-8 -*-
#
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
#

import sys
import os
import os.path

abspath = os.path.dirname(__file__)
if abspath is not None and abspath != "":
    sys.path.append(abspath)
    sys.path.append('../')
    os.chdir(abspath)


try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)


try:
    from dc2.lib.db.mongo import MongoStore
    from dc2.lib.auth.helpers import get_realname
    from dc2.lib.auth.helpers import check_membership_in_group
except ImportError, e:
    print "Your DC2 installation is not correct"
    print e
    sys.exit(1)
#
# Apps Import
#
try:
    from dc2.admincenter.apps import MainAppHandler
except ImportError, e:
    print "You didn't install DC² correctly"
    print e
    sys.exit(1)

try:
    from settings import MONGOS
    from settings import GRP_NAME_DC2ADMINS
    from settings import KERBEROS_AUTH_ENABLED
except ImportError, e:
    print 'You do not have a settings file.'
    sys.exit(1)


urls = (
    "(.*)", 'MainAppHandler',
    # "/login","Login",
    # '/admin',admin.app_admin
)

session_db = MONGOS["admincenter"]["database"].get_db()

app = web.application(urls, globals(), autoreload=True)
sessions = web.session.Session(app, MongoStore(session_db, 'sessions'))


def session_hook():
    web.ctx.session = sessions


def is_admin():
    if 'authenticated' in web.ctx.session:
        if web.ctx.session.authenticated:
            web.ctx.session.realname = get_realname(web.ctx.session.username)
            web.ctx.session.is_dc2admin = check_membership_in_group(
                web.ctx.session.username, GRP_NAME_DC2ADMINS)


def set_kerberos_data():
    if KERBEROS_AUTH_ENABLED:
        if 'krb5ccname' in web.ctx.session:
            web.ctx.env['KRB5CCNAME'] = web.ctx.session.krb5ccname
            os.environ['KRB5CCNAME'] = web.ctx.session.krb5ccname


app.add_processor(web.loadhook(session_hook))
app.add_processor(web.loadhook(is_admin))
app.add_processor(web.loadhook(set_kerberos_data))

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
