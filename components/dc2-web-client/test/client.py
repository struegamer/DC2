#!/usr/bin/env python2.7

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace

class CommandNamespace(BaseNamespace):

	def on_connect(self):
		print('connected')

	def on_disconnect(self):
		print('disconnected')
	
	def on_discovered_response(self, *args):
		print(args)
	

if __name__ == '__main__':
	socketio = SocketIO('localhost', 5000)
	command_ns = socketio.define(CommandNamespace, '/commands')
	command_ns.emit('discovered',{'whatever':'is here'})
	socketio.wait(seconds=10)

