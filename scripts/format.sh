#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --in-place msaSDK docs_src --exclude=__init__.py
black msaSDK docs_src
isort msaSDK docs_src
