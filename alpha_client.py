#!/usr/bin/env python3
import time
import re
import socket
import sys
import os

server = '{{ server_address  }}'
port = {{ server_port }}
auth_log = '/var/log/auth.log'

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def report(host,port,attempt_count):
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(attempt_count.encode())
        print("Data sent to server")

    except socket.error as msg:
        print("Socket closed %s" % str(msg))
    s.close()

def main():
    logfile = open(auth_log,"r")
    loglines = follow(logfile)
    for line in loglines:
        if re.match('.*sshd.*?(Failed|Connection\sclosed|Accepted).*',line) is not None:
            report(server, port, '1')

if __name__ == '__main__':
    pid = str(os.getpid())
    pidfile = "/tmp/mydaemon.pid"
    if os.path.isfile(pidfile):
        print("%s already exists, exiting" % pidfile)
        sys.exit(0)
    open(pidfile, 'w').write(pid)
    try:
        main()
    finally:
        os.unlink(pidfile)

