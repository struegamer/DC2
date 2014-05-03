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

try:
    from dc2.web.live.startup import socketio
    from flask.ext.socketio import emit
except ImportError as e:
    print(e)
    print(__file__)
    sys.exit(1)


@socketio.on('connect', namespace='/commands')
def on_commands_connect():
    print('connected')
    print(dir(socketio))
    pass


@socketio.on('disconnect', namespace='/commands')
def on_commands_disconnect():
    pass


@socketio.on('discovered', namespace='/commands')
def on_commands_discovered(message):
    emit('discovered_device', message, namespace='/updates')
