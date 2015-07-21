#!/usr/bin/env python2

from distutils.core import setup

setup(name='blaunch',
	version='0.1',
	description='Simple program launcher',
	author='Tiltar',
	author_email='tiltar7@gmail.com',
	url='https://github.com/Tiltar/blaunch',
	packages=['blaunch'],
	scripts=['bin/blaunch'],
	data_files=[('/etc/blaunch', ['etc/blaunch.conf', 'etc/menu.conf'])],
	requires=['wxpython']
	)
