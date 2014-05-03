#!/usr/bin/env python2.7

import sys

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace

class CommandNamespace(BaseNamespace):
	pass

class UpdatesNamespace(BaseNamespace):

	def on_connect(self):
		print('connected')

	def on_disconnect(self):
		print('disconnected')
	
	def on_discovered_device(self, data, *args):
		print(data)
		print(args)
	

if __name__ == '__main__':
	message = sys.argv[1]
	socketio = SocketIO('localhost', 5000)
	command_ns = socketio.define(CommandNamespace, '/commands')
	updates_ns = socketio.define(UpdatesNamespace, '/updates')
	command_ns.emit('discovered',{'message':message})
	socketio.wait(seconds=0.5)

