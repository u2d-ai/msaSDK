# -*- coding: utf-8 -*-

import os

from server.srv_uvicorn import MSAServerUvicorn

if __name__ == '__main__':
    pass

ROOTPATH = os.path.join(os.path.dirname(__file__))


def run():
    server_runner = MSAServerUvicorn(app="app:app", app_dir=ROOTPATH, host="127.0.0.1", port=8090)
    server_runner.run()
