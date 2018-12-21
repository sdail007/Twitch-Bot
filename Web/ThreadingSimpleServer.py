import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import threading

class ThreadingSimpleServer(SocketServer.ThreadingMixIn,
                            BaseHTTPServer.HTTPServer):

    _Instance = None

    @classmethod
    def Start(cls):
        if cls._Instance is None:
            _Instance = ThreadingSimpleServer(('', 8000),
                                              SimpleHTTPServer.SimpleHTTPRequestHandler)

            webServerThread = threading.Thread(target=_Instance.serve_forever)
            webServerThread.daemon = True
            webServerThread.start()

    pass
