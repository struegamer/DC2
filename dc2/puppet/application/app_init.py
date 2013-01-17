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
    from flask import Flask, g
except ImportError as e:
    print('Flask is not installed')
    print(e)
    sys.exit(1)

from dc2.puppet.db import connect_db
from dc2.puppet.db import disconnect_db

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = connect_db(app)

from dc2.puppet.bp import BPClasses

app.register_blueprint(BPClasses, url_prefix='/RPC')

