import os

import prometheus_client
import prometheus_client.multiprocess
import gunicorn

from prometheus_client import multiprocess

pythonpath = "/app/src"

bind = ["0.0.0.0:80"]
workers = 10
timeout = 2000

proc_name = "backend-service-gunicorn"
loglevel = "info"
logfile = "/var/log/app/gunicorn.log"
accesslog = "/var/log/app/access.log"

gunicorn.SERVER_SOFTWARE = "backend_server"

STR_TO_BOOL = {"True": True, "False": False}

DEBUG = STR_TO_BOOL.get(os.getenv("DEBUG"), False)


def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)


def on_starting(server):
    registry = prometheus_client.CollectorRegistry()
    prometheus_client.multiprocess.MultiProcessCollector(registry)
    prometheus_client.start_http_server(9000, registry=registry)
