from http.server import HTTPServer

from lib.threading2 import LoggingExceptionsThread
from controls.base import Component
from controls.rc_web import Web
from config import Config
from pathlib import Path


class RC(Component, LoggingExceptionsThread):
    """
        Cars remote controls via local HTTPServer.
        * output = responding GET requests by giving WebPage content
        * input = responding POST requests from WebPage buttons > translate to actions for engine actuator
    """
    def __init__(self, control) -> None:
        super().__init__()
        LoggingExceptionsThread.__init__(self)
        Web._control = control
        self.webServer = None

    def stop(self):
        super().stop()
        self.webServer.server_close()
        self.webServer.shutdown()

    def iterate(self):
        if Path.exists(Path('/home/pi')):
            self.webServer = HTTPServer(Config.RC_HTTP_SERVER, Web)
        else:
            self.logger.info(f'Faking web server to {Config.LOCAL_RC_HTTP_SERVER}')
            self.webServer = HTTPServer(Config.LOCAL_RC_HTTP_SERVER, Web)
        self.webServer.serve_forever()  # blocking, iterates only to log exceptions from HTTPServer = no iteration period set/expected
