# coding:utf-8
# client.py

import json
import time
import struct
import socket


def rpc(sock, route, params):
    request = json.dumps({'route': route, 'params': params})
    length_prefix = struct.pack("I", len(request))
    sock.sendall(length_prefix)
    sock.sendall(request)
    length_prefix = sock.recv(4)
    length, = struct.unpack("I", length_prefix)
    body = sock.recv(length)
    response = json.loads(body)
    return response['out'], response['result']


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    '''
    for i in range(10):
        out, result = rpc(s, "ping", "pi %d" %i)
        print out, result
        time.sleep(1)
    '''

    # out, result = rpc(s, "ping", "pi 1")
    # out2, result = rpc(s, "fab", "10")
    out3, result = rpc(s, "rput", "a,123")
    out4, result = rpc(s, "rget", "a")
    # print out2, result
    print out3, result
    print out4, result
    s.close()