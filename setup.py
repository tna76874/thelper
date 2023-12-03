
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from setuptools import find_packages, setup

import thelper

setup(
    name='thelper',
    version=thelper.__version__,
    description='Teacher helper tools',
    url='https://github.com/tna76874/thelper.git',
    author='lmh',
    author_email='',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=[
        "Jinja2",
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9',
    ],
    python_requires = ">=3.8",
    entry_points={
        "console_scripts": [
            "thelper = thelper.thelper:main",
        ],
    },
    )