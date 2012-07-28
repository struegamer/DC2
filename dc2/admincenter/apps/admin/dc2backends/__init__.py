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

try:
    import web
except ImportError,e:
    print "You didn't install web.py"
    print e
    sys.exit(1)

try:
    from dc2.admincenter.globals import ADMIN_MODULES
except ImportError,e:
    print "You don't have this DC2 module.."
    print e
    sys.exit(1)

ADMIN_MODULES.append({'title':'DC2 Backends','url':'/admin/backends'})

from main import ActionIndex
from main import ActionAdd
from main import ActionDelete
from main import ActionREST

urls=(
    '(.*)','ActionIndex',
)

app_admin_dc2backends=web.application(urls,locals())
