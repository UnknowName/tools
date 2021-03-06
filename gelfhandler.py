#!/bin/env python
# coding:utf8


import re
import sys
import zlib
import json
import socket
from logging.handlers import DatagramHandler

PY_VERSION = sys.version_info[0]


def _check_ip(ip):
    p = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
        '(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
    )
    if p.match(ip):
        return True
    else:
        return False


class GELFHandler(DatagramHandler):
    "GELF Log Format Logging Handler"
    hostname = socket.gethostname()

    def __init__(self, host, port=12201):
        DatagramHandler.__init__(self, host, port)
        if _check_ip(host):
            pass
        else:
            print('Please Check IP!')
            raise Exception

    def makePickle(self, record):
        log_dic = dict(
            version="1.1",
            message=record.msg,
            module=record.module,
            source=self.hostname,
            logerName=record.name,
            level=record.levelname,
            fileName=record.filename,
            threadName=record.threadName
        )
        log = json.dumps(log_dic)
        if PY_VERSION == 3:
            compres_str = zlib.compress(bytes(log, encoding='utf8'))
        else:
            compres_str = zlib.compress(log)
        return compres_str


if __name__ == '__main__':
    import logging
    loger = logging.getLogger('test-log')
    gh = GELFHandler('192.168.11.225', 12201)
    loger.setLevel(logging.DEBUG)
    gh.setLevel(logging.DEBUG)
    loger.addHandler(gh)
    loger.info('2测试日志，来自GELFHander日志系统')
