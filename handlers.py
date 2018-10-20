#coding:utf-8

from sim_redis import SimRedis


def redis_get(conn, param, response):
    sim_redis = SimRedis()
    out = sim_redis.get(param)
    response(conn, out, param)


def redis_put(conn, param, response):
    try:
        key, value = param.split(',')
    except ValueError:
        return "BAD REQUEST"
    sim_redis = SimRedis()
    out = sim_redis.insert(key, value)
    response(conn, out, param)