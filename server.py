# -*- coding: utf-8 -*-
# ----------------------------
# @File    : server.py
# @Date    : 2021-04-16
# @Author  : jf.l
# ----------------------------



from flask_sockets import Sockets
import datetime
import time
from flask import Flask
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.exceptions import WebSocketError
from blinker import signal

app = Flask(__name__)
sockets = Sockets(app)


class SignalPool:
    def __init__(self):
        self.pool = {}

    def get(self, signal_name):
        s = self.pool.setdefault(signal_name, signal(signal_name))
        return s


sp = SignalPool()


@sockets.route('/echo')
def echo_socket(ws):
    name = ws.receive()
    print(name)

    def send_(sender):

        try:
            ws.send(sender)  # 发送数据
        except WebSocketError as e:
            print(ws, " is disconnect")
            sp.get(name).disconnect(send_) # 取消订阅

    sp.get(name).connect(send_)
    while not ws.closed:
        # nothing to do, just keep socket alive
        time.sleep(30)


@app.route('/<name>')
def hello(name):
    now = datetime.datetime.now().isoformat() + 'Z'
    s = sp.get(name)
    s.send(name + str(now))
    return 'Hello {name}!'.format(name=name)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5005), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()

#
