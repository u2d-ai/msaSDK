#!/usr/bin/env bash

set -e
set -x

mypy msaSDK
flake8 msaSDK docs_src
black msaSDK docs_src --check
isort msaSDK docs_src scripts --check-only

