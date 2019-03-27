"""
 @file
 @brief This file connects to libopenshot and logs debug messages (if debug preference enabled)

 """

from threading import Thread
from classes import settings, info
from classes.logger import log
import openshot
import os
import zmq


class LoggerLibOpenShot(Thread):

    def kill(self):
        self.running = False

    def run(self):
        # Running
        self.running = True

        # Get settings
        s = settings.get_settings()

        # Get port from settings
        port = s.get("debug-port")
        debug_enabled = s.get("debug-mode")

        # Set port on ZmqLogger singleton
        openshot.ZmqLogger.Instance().Connection("tcp://*:%s" % port)

        # Set filepath for ZmqLogger also
        openshot.ZmqLogger.Instance().Path(os.path.join(info.USER_PATH, 'libopenshot.log'))

        # Enable / Disable logger
        openshot.ZmqLogger.Instance().Enable(debug_enabled)

        # Socket to talk to server
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, '')

        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        log.info("Connecting to libopenshot with debug port: %s" % port)
        socket.connect ("tcp://localhost:%s" % port)

        while self.running:
            msg = None

            # Receive all debug message sent from libopenshot (if any)
            socks = dict(poller.poll(1000))
            if socks:
                if socks.get(socket) == zmq.POLLIN:
                    msg = socket.recv(zmq.NOBLOCK)

            # Log the message (if any)
            if msg:
                log.info(msg.strip().decode('UTF-8'))