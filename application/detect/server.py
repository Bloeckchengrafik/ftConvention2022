from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from logging import getLogger, info
from queue import Queue
import cv2 as cv
import numpy as np
import base64

inqueue = Queue()
outqueue = Queue()

class WebSocketServer(WebSocket):
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)

        socketserver = lambda: self.loadImage()

        self.log = getLogger("websocket")


    def data_uri_to_cv2_img(self,uri):
        encoded_data = uri.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        return img

    def handleMessage(self):
        outqueue.put_nowait(self.data_uri_to_cv2_img(self.data))
    
    def loadImage(self):
        for client in self.server.connections.values():
            client.sendMessage("pls img\n")

    def handleConnected(self):
        self.log.info(f"'{self.address[0]}:{self.address[1]}' connected to WS")

    def handleClose(self):
        self.log.info(f"'{self.address[0]}:{self.address[1]}' disconnected from WS")

def run():
    server = SimpleWebSocketServer('', 8000, WebSocketServer)
    while True:
        server.serveonce()
        if len(server.connections.keys()) == 0:
            continue

        if inqueue.empty():
            continue

        server.connections[list(server.connections.keys())[0]].loadImage()
        inqueue.get_nowait()
