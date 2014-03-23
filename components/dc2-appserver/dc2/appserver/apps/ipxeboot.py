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


#
# Standard Python libs
#
import sys

#
# web.py module
#

try:
    import web
except ImportError:
    print "You need to install web.py"
    sys.exit(1)


try:
    from settings import DOWNLOAD_SERVER_URL
    from settings import XMLRPC_BACKEND_SERVER_IP
except ImportError:
    print "You don't have a settings file in your Python path"
    sys.exit(1)


class IPXEBoot:
        def GET(self, name):
            result = ""
            if name is None or name == "":
                result = "#!ipxe\n\n"
                result += ":retry_dhcp\n"
                result += "dhcp || goto retry_dhcp\n"
                result +=\
                    "set 209:string http://{0}/boot/pxelinux.cfg/'\
                    '01-${mac:hexhyp}\n".\
                    format(XMLRPC_BACKEND_SERVER_IP)
                result += "set 210:string {0}/\n".format(DOWNLOAD_SERVER_URL)
                result += "chain pxelinux.0\n"
            web.header("Content-Type", "text/plain")
            return result
