#!/usr/bin/env python

import xmlrpclib

from dc2.web.live.startup import app
from dc2.web.live.startup import socketio
from flask.ext.restful.utils import cors


from dc2.web.live.api.v1.rest_dhcp import *  # noqa
from dc2.web.live.socket_handlers.clients import *  # noqa
from dc2.web.live.socket_handlers.commands import *  # noqa

app.config['DC2Backend'] = xmlrpclib.ServerProxy(
    'http://dc2db.lax-stg1.stg.gaikai.net/RPC', allow_none=True)

if __name__ == '__main__':

    api.init_app(app)
    api.method_decorators = [cors.crossdomain(
        origin='*',
        automatic_options=True)]

    socketio.init_app(app)
    socketio.run(app, heartbeat_interval=2, heartbeat_timeout=5)
