#!/usr/bin/env bash

set -e

python setup.py sdist
twine upload dist/*