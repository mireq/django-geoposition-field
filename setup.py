# -*- coding: utf-8 -*-

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

def get_packages(package):
	return [dirpath
		for dirpath, dirnames, filenames in os.walk(package)
		if os.path.exists(os.path.join(dirpath, '__init__.py'))]


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-geoposition-field',
	version='0.1',
	packages=get_packages('django_geoposition_field'),
	include_package_data=True,
	license='BSD License',
	description='Django email logger',
	long_description=README,
	url='https://github.com/mireq/django-geoposition-field',
	author='Miroslav Bendik',
	author_email='miroslav.bendik@gmail.com',
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)

