#!/usr/bin/env python3

import os

import bottle
import redis

# https://github.com/prometheus/client_python/issues/250
os.environ["prometheus_multiproc_dir"] = ".metrics"
import prometheus_client as prom
from prometheus_client import multiprocess

# Bottle
app = bottle.Bottle()

# Redis
r = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", default="redis"),
    port=os.getenv("REDIS_PORT", default=6379), # Importnat to add explicitly REDIS_PORT in yml env https://github.com/docker-library/redis/issues/53
    password=os.getenv("REDIS_PASSWORD"),
)

# Prometheus
prom_registry = prom.CollectorRegistry()
multiprocess.MultiProcessCollector(prom_registry)
prom_request = prom.Counter(
    "http_requests_total", "total http requests", ["method", "endpoint", "status_code"]
)


@app.post("/hit")
def hit():
    try:
        r.incr("hit", 1)
    except redis.exceptions.RedisError:
        status_code = 500
        message = "failed to connect to redis"
    else:
        status_code = 201
        message = "ok"
    bottle.response.status = status_code
    prom_request.labels(method="post", endpoint="hit", status_code=status_code).inc()
    return message


@app.get("/total")
def total():
    try:
        total = r.get("hit") or "0"
    except redis.exceptions.RedisError:
        status_code = 500
        message = "failed to connect to redis"
    else:
        status_code = 200
        message = total
    bottle.response.status = status_code
    prom_request.labels(method="get", endpoint="total", status_code=status_code).inc()
    return message


@app.get("/health/liveness")
def health_liveness():
    bottle.response.status = 200
    return "ok"


@app.get("/health/readiness")
def health_readiness():
    try:
        r.ping()
    except redis.exceptions.RedisError:
        bottle.response.status = 500
        message = "failed to connect to redis"
    else:
        bottle.response.status = 200
        message = "ok"
    return message


@app.get("/_metrics")
def metrics():
    return prom.generate_latest(prom_registry)


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", default="0.0.0.0"),
        port=os.getenv("PORT", default="8080"),
    )
