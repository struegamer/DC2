#!/usr/bin/env python2.7

import sys

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace

import logging
logging.basicConfig(level=logging.DEBUG)

class CommandNamespace(BaseNamespace):

    def on_command_error(self, data, *args):
        print(data)

class UpdatesNamespace(BaseNamespace):

    def on_connect(self):
        print('connected')

    def on_disconnect(self):
        print('disconnected')
	
    def on_discovered_device(self, data, *args):
        print(data)


if __name__ == '__main__':
    message = sys.argv[1]
    socketio = SocketIO('localhost', 5000)
    command_ns = socketio.define('CommandNamespace', '/commands')
    updates_ns = socketio.define(UpdatesNamespace, '/updates')
    command_ns.emit('discovered',{
        'cluster_no': '01',
        'rack_no': 'r1',
        'dcname': 'laxa'
        })
    socketio.wait(seconds=0.5)

