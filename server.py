# coding: utf-8
# author: yuwhuawang

import json
import struct
import socket


def handle(conn, addr, handlers):
    print ("{} comes".format(addr))
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print("{}, bye".format(addr))
            conn.close()
            break
        length, = struct.unpack("i", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        route = request['route']
        params = request['params']
        print route, params
        handler = handlers[route]
        handler(conn, params)


def run_forever(sock, handlers):
    while True:
        conn, addr = sock.accept()
        handle(conn, addr, handlers)


def pinghandler(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({'out': out, 'result': result})
    length_prefix = struct.pack("I", len(response))
    conn.sendall(length_prefix)
    conn.sendall(response)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 9000))
    sock.listen(1)
    handlers = {
        "ping": pinghandler
    }

    run_forever(sock, handlers)



