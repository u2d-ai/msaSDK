# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 SWelcker
"""
import os
from os import path

from loguru import logger

if __name__ == "__main__":
    from msaServer import base
    root_path: str = path.join(os.path.dirname(__file__))
    logger.info("Starting msaSDK Services...")
    base.run(app_dir=root_path)
