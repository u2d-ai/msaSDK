# -*- coding: utf-8 -*-

import multiprocessing
import os
import logging
import sys
from abc import ABC

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from loguru import logger

from msaSDK.service import MSAApp

if __name__ == '__main__':
    pass

JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


def number_of_workers():
    ret = (multiprocessing.cpu_count())
    if ret > 10: ret = 10
    ret = int(os.environ.get("GUNICORN_WORKERS", str(ret)))
    return ret


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def __init__(self, cfg, log_level: str = "info"):
        super().__init__(cfg=cfg)

        self.handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(self.handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(self.handler)
        self.log_level: str = log_level
        self.error_logger.setLevel(self.log_level)
        self.access_logger.setLevel(self.log_level)


class StandaloneApplication(BaseApplication, ABC):
    def __init__(self, app: MSAApp, options=None):
        self.options = options or {}
        self.application: MSAApp = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class MSAServerGunicorn:

    def __init__(self, app: MSAApp, app_dir: str, host: str, port: int, reload: bool = False, log_level: str = "info",
                 workers: int = -1) -> None:
        super().__init__()
        self.app: MSAApp = app
        self.app_dir: str = app_dir
        self.port: int = port
        self.host: str = host
        self.reload: bool = reload
        self.log_level: str = log_level
        self.workers: int = workers
        if self.workers < 1:
            self.workers = number_of_workers()
        self.intercept_handler = InterceptHandler()
        logging.root.setLevel(self.log_level)
        # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
        # logging.root.handlers = [intercept_handler]
        self.seen = set()

    def run(self):

        for name in [
            *logging.root.manager.loggerDict.keys(),
            "gunicorn",
            "gunicorn.access",
            "gunicorn.error",
            "uvicorn",
            "uvicorn.access",
            "uvicorn.error",
        ]:
            if name not in self.seen:
                self.seen.add(name.split(".")[0])
                logging.getLogger(name).handlers = [self.intercept_handler]

        logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

        options = {
            'bind': '%s:%s' % (self.host, self.port),
            'reload': self.reload,
            'workers': self.workers,
            'worker_class': 'uvicorn.workers.UvicornWorker',
            'accesslog': '-',
            'errorlog': '-',
            "logger_class": StubbedGunicornLogger
        }

        StandaloneApplication(self.app, options).run()
