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


import xmlrpclib
import types

from helper import *


def xenserver_login(xenhost=None, xenuser=None, xenpw=None):
    if xenhost is not None and xenuser is not None and xenpw is not None:
        try:
            s = xmlrpclib.ServerProxy("https://%s/" % xenhost)
            session_id = parse_output(s.session.login_with_password(xenuser, xenpw))
            return session_id
        except Exception, e:
            return xmlrpclib.Fault(500, "Exception: %s" % e)
    return None

def xenserver_logout(xenhost=None, session_id=None):
    if xenhost is not None and session_id is not None:
        s = xmlrpclib.ServerProxy("https://%s/" % xenhost)
        s.session.logout(session_id)
        return True
    return False
