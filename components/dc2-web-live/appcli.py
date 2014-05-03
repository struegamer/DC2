

import sys
sys.path.insert(0, '.')

from dc2.web.live.startup import app
from dc2.web.live.startup import socketio
from dc2.web.live.socket_handlers.commands import *

if __name__ == '__main__':
    socketio.run(app)
