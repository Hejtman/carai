from http.server import HTTPServer

from lib.threading2 import ComponentThread
from controls.rc_web import Web
from config import Config


class RC(ComponentThread):
    """
        Cars remote controls via local HTTPServer.
        * output = responding GET requests by giving WebPage content
        * input = responding POST requests from WebPage buttons > translate to actions for engine actuator
    """
    def __init__(self, control) -> None:
        super().__init__(period=float('inf'))  # component status = running after first iteration...forever
        Web._control = control
        self.webServer = None

    def start(self) -> None:
        self.webServer = HTTPServer(Config.RC_HTTP_SERVER, Web)
        super().start()  # start iterating

    def stop(self):
        super().stop()  # stop iterating
        self.period = 0  # component status = stopped
        self.webServer.server_close()
        self.webServer.shutdown()

    def iterate(self):
        self.webServer.serve_forever()  # blocking, iterates only to log exceptions from HTTPServer
