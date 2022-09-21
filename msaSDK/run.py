# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 SWelcker
"""
from loguru import logger

if __name__ == "__main__":
    from msaSDK import main

    logger.info("Starting msaSDK Services...")
    main.run()
