# coding:utf-8

import os
import struct
import socket
import json
from sim_redis import SimRedis


def handle_conn(conn, addr, handlers):
    print addr, "comes"
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print(addr, "bye")
            conn.close()
            break
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        in_ = request['route']
        params = request['params']
        print (in_, params)
        handlers[in_](conn, params)


def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()
        pid = os.fork()
        if pid < 0:
            return
        if pid > 0:
            conn.close()
            continue
        if pid == 0:
            sock.close()
            handle_conn(conn, addr, handlers)
            break


def send_result(conn, out, result):
    response = json.dumps({'out': out, "result":result})
    length_prefix = struct.pack("I", len(response))
    conn.sendall(length_prefix)
    conn.sendall(response)


def redis_get(conn, param):
    sim_redis = SimRedis()
    out = sim_redis.get(param)
    send_result(conn, out, param)


def redis_insert(conn, param):
    try:
        key, value = param.split(',')
    except ValueError:
        return "BAD REQUEST"
    sim_redis = SimRedis()
    out = sim_redis.insert(key, value)
    send_result(conn, out, param)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(1)
    handlers = {
        "rget": redis_get,
        "rput": redis_insert
    }

    loop(sock, handlers)
