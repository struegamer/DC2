# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

import sys
import json

from dc2.web.live.startup.globals import app
from dc2.web.live.startup.globals import api
from dc2.web.live.startup.globals import socketio

try:
    from flask import request
    from flask.ext.restful import Resource as RestResource
    from flask.ext.restful.utils import cors
except ImportError as e:
    print('{0}: {1}'.format(__file__, e))
    sys.exit(1)


class RestEvents(RestResource):

    @cors.crossdomain(origin="*")
    def post(self):
        pass


class EventDiscoveredRack(RestEvents):

    @cors.crossdomain(origin="*")
    def post(self):
        print(request.json)
        return request.json, 200

api.add_resource(EventDiscoveredRack, '/api/v1/events/discover/racks')
