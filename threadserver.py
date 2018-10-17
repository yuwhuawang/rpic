# coding: utf-8

import json
import struct
import socket
import thread
from sim_redis import SimRedis

def handle_conn(conn, addr, handlers):
    print addr, "comes"
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print addr, "bye"
            conn.close()
            break
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        in_ = request['route']
        param = request['params']
        print in_, param
        handler = handlers[in_]
        handler(conn, param)
    pass


def loop(sock, handlers):
    """
    run server in an infinite loop, open a thread to handle each thread
    :param sock:
    :param hanlder:
    :return:
    """
    while True:
        conn, addr = sock.accept()
        thread.start_new_thread(handle_conn, (conn, addr, handlers))


def ping(conn, params):
    send_result(conn, "pong", params)


def fab_handler(conn, params):
    try:
        max = int(params)
        out = list(fab(max))
    except ValueError:
        out = "bad request"
    send_result(conn, out, params)


def redis_get(conn, params):
    sim_redis = SimRedis()
    out = sim_redis.get(params)
    send_result(conn, out, params)


def redis_insert(conn, params):
    try:
        key, value = params.split(',')
    except  ValueError, TypeError:
        return "BAD REQUEST"
    sim_redis = SimRedis()
    out = sim_redis.insert(key, value)
    send_result(conn, out, params)


def fab(max):
    first, second, n = 0, 1, 0
    while n < max:
        yield second
        first, second = second, first + second
        n += 1


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result})
    length_prefix = struct.pack("I", len(response))
    conn.sendall(length_prefix)
    conn.sendall(response)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 8080))
    sock.listen(1)
    handlers = {
        "ping": ping,
        "fab": fab_handler,
        "r_get": redis_get,
        "r_insert": redis_insert
    }
    loop(sock, handlers)




