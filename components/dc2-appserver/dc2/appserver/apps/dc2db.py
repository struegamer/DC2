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
import os
import os.path
import shutil

#
# web.py module
#

try:
    import web
except ImportError:
    print "You need to install web.py"
    sys.exit(1)

#
# DC² own modules
#
try:
    from dc2.appserver.globals import requestdispatcher
except ImportError as e:
    print(e)
    print "You are missing necessary DC² modules"
    print e
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
    from settings import ACCESS_CONTROL_ALLOW_ORIGIN
    from settings import ACCESS_CONTROL_ALLOW_METHODS
    from settings import FREEIPA_ENABLED
    from settings import KERBEROS_AUTH_ENABLED
except ImportError:
    print "You don't have a settings file in your Python path"
    sys.exit(1)


class DC2DB:
    def GET(self):
        listmethods = web.template.frender("%s/methodList.tmpl" % TEMPLATE_DIR)
        result = listmethods(requestdispatcher.list_rpc_methods())
        web.header("Content-Type", "text/html")
        web.header("Access-Control-Allow-Origin", ACCESS_CONTROL_ALLOW_ORIGIN)
        web.header(
            "Access-Control-Allow-Methods",
            ACCESS_CONTROL_ALLOW_METHODS)
        return result

    def POST(self):
        content_type = web.ctx.env.get("CONTENT_TYPE")
        content_type = content_type.split(";")[0]
        if content_type.find("xml") != -1:
            content_type = "xmlrpc"
        if content_type.find("json") != -1:
            content_type = "jsonrpc"
        if content_type.find("application/x-www-form-urlencoded") != -1:
            content_type = "jsonrpc"
        if FREEIPA_ENABLED and KERBEROS_AUTH_ENABLED:
            if 'KRB5CCNAME' in web.ctx.env:
                filename = web.ctx.env['KRB5CCNAME']
                filename = filename.split(':')[1]
                shutil.copyfile(
                    '{0}'.format(filename),
                    '/tmp/krb5ccname-{0}'.format(web.ctx.env['REMOTE_USER']))
                os.environ['KRB5CCNAME'] = web.ctx.env['KRB5CCNAME']
            else:
                if 'REMOTE_USER' in web.ctx.env:
                    os.environ['KRB5CCNAME'] =\
                        'FILE:/tmp/krb5ccname-{0}'.format(
                            web.ctx.env['REMOTE_USER'])
        return_data = requestdispatcher.handle_request(
            content_type,
            web.data())
        web.header("Content-Type", return_data[0])
        web.header("Access-Control-Allow-Origin", ACCESS_CONTROL_ALLOW_ORIGIN)
        web.header(
            "Access-Control-Allow-Methods",
            ACCESS_CONTROL_ALLOW_METHODS)
        return return_data[1]

    def OPTIONS(self):
        web.header("Content-Type", "text/plain")
        web.header("Access-Control-Max-Age", "0")
        web.header("Access-Control-Allow-Origin", ACCESS_CONTROL_ALLOW_ORIGIN)
        web.header(
            "Access-Control-Allow-Methods",
            ACCESS_CONTROL_ALLOW_METHODS)
        web.header("Access-Control-Allow-Headers", web.ctx.env.get(
            "HTTP_ACCESS_CONTROL_REQUEST_HEADERS"))
        return "true"
