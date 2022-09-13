#!/usr/bin/env python
from setuptools import setup, find_packages


# Parse version number from pyglet/__init__.py:
with open('u2d_msa_sdk/__init__.py') as f:
    info = {}
    for line in f:
        if line.startswith('version'):
            exec(line, info)
            break


setup_info = dict(
    name='u2d_msa_sdk',
    version=info['version'],
    author='Stefan Welcker',
    author_email='stefan@u2d.ai',
    url='http://msa.u2d.ai/',
    download_url='http://pypi.python.org/pypi/u2d_msa_sdk',
    project_urls={
        'Documentation': 'http://msa.u2d.ai/',
        'Source': 'https://github.com/swelcker/U2D_MSA_SDK',
        'Tracker': 'https://github.com/swelcker/U2D_MSA_SDK/issues',
    },
    description='FastAPI based Microservice Architecture Development Kit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=['u2d_msa_sdk'] + ['u2d_msa_sdk.' + pkg for pkg in find_packages('u2d_msa_sdk')],

    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,
)

setup(**setup_info)