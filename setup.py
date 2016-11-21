#!/usr/bin/env python2

from distutils.core import setup

setup(
    name='blaunch',
    version='0.1',
    description='Simple program launcher',
    author='Brian Steffens',
    url='https://github.com/briansteffens/blaunch',
    packages=['blaunch'],
    scripts=['bin/blaunch'],
    data_files=[('/etc/blaunch', ['etc/blaunch.conf', 'etc/menu.conf'])],
    requires=['wxpython']
)
