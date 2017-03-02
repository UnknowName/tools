#!/bin/env python
# coding:utf8


import time
import gzip
import json
from threading import Thread
from cStringIO import StringIO
from SocketServer import BaseRequestHandler, ThreadingUDPServer


class GraylogHandler(BaseRequestHandler):
    def handle(self):
	msg, _ = self.request
	buf = StringIO(msg)
	f = gzip.GzipFile(fileobj=buf)
	gelf_log = json.loads(f.read())
	log = gelf_log['full_message'].encode('utf8')
	with open('app.log', 'a') as f:
	    f.write(log+'\n')


if __name__ == '__main__':
	serv = ThreadingUDPServer(('', 12201), GraylogHandler)
	serv.serve_forever()


