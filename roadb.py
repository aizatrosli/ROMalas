from adb.client import Client as adbc
import numpy as np
import threading
import cv2
import __main__

'''
Nox command
Nox.exe -resolution:1440x900 -dpi:270 -package:com.bignox.app.test
'''
ssdb = {
    'bar' : {"health_bar" : [123,124,42,136,1],"mana_bar" : [135,136,42,136,0],"base_bar" : [712,713,54,636,0], "job_base" : [712,713,644,1226,0]},
    'poskey' : {"skill6":[0x4ca,0x28b],"skill5":[0x46c,0x28b],"skill4":[0x0a,0x28b],"skill3":[0x3aa,0x28b],"skill2":[0x348,0x28b],"skill1":[0x2e8,0x28b],"auto":[0x4ca,0x22b],"item5":[0x46c,0x22b],"item4":[0x40a,0x22b],"item3":[0x3aa,0x22b],"item2":[0x348,0x22b],"item1":[0x2e8,0x22b]},
    'posmap' : {"map":[0x4ee,0x57],"world":[0x36f,0x23c],"minitopleft":[0x340,0xc8],"minibtmleft":[0x340,0x215],"minitopright":[0x4d5,0xc8],"minibtmright":[0x4d5,0x215]},
    'submenu' : {"allmon":[0x3eb,0x11d]}
}

class adbconnect(objects):

    def __init__(self, ip='127.0.0.1', port=5037):
        self.client = None
        self.device = None
        self.ip = ip
        self.port = port
        self.connect()
        self.ssstart()

    def connect(self):
        try:
            self.client = adbc(host=self.ip, port=self.port)
            self.device = self.client.device("{0}:62001".format(ip))
        except Exception as e:
            print e

    def screenshotpool(self, device):
        ssthread = threading.currentThread()
        while getattr(ssthread, "pooling", True):
            imgbytearr = device.screencap()
            setattr(__main__, 'ssbyte', imgbytearr)
            imgarr = cv2.imdecode(np.fromstring(bytes(imgbytearr), np.uint8), cv2.IMREAD_COLOR)
            setattr(__main__, 'ssimg', imgarr)

    def ssstart(self):
        ssthread = threading.Thread(target=self.screenshotpool, args=(self.device,))
        setattr(__main__, 'ssthread', ssthread)
        __main__.ssthread.start()

    def ssend(self):
        __main__.ssthread.pooling = False
        __main__.ssthread.join()

    def barpool(self):
        barthread = threading.currentThread()
        while getattr(barthread, "pooling", True):




