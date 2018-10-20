#coding: utf-8

import os
import struct
import json
import socket
from handlers import redis_get, redis_put


def handle_conn(conn, addr, handlers):
    print (addr, "comes")
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print (addr, "bye")
            conn.close()
            break
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        route = request['route']
        param = request['params']
        print route, param
        handlers[route](conn, param, reponse)


def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()
        handle_conn(conn, addr, handlers)


def reponse(conn, out, result):
    res = json.dumps({"out": out, "result": result})
    length_prefix = struct.pack("I", len(res))
    conn.sendall(length_prefix)
    conn.sendall(res)


def prefork(n):
    for i in range(n):
        pid = os.fork()
        if pid < 0:
            return
        if pid > 0:
            continue
        if pid == 0:
            break


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(1)
    prefork(10)
    handlers = {
        'rget': redis_get,
        'rput': redis_put
    }
    loop(sock, handlers)



