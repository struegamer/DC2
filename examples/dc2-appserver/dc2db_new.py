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
    os.chdir(abspath)


try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)


try:
    from dc2.appserver.apps import DC2DB
    from dc2.appserver.apps import IPXEBoot
    from dc2.appserver.apps import BootServer
except ImportError:
    print "You didn't install DC² correctly"
    sys.exit(1)

urls = ("/RPC", "DC2DB",
        "/boot/(.*)", "BootServer",
        "/ipxe/(.*)", "IPXEBoot")


app = web.application(urls, globals(), autoreload=True)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
