===============================================
Django simple geoposition field with OSM widget
===============================================

|codecov| |version| |downloads| |license|

This package adds geoposition field with map widget to django. It don't deppend
on GIS extensions.

Install
-------

.. code:: bash

	pip install django-easy-geoposition-field

Usage
-----

Add ``django_geoposition_field`` to ``INSTALLED_APPS``.

.. code:: python

	# settings.py
	INSTALLED_APPS = (
		# ...
		'django_geoposition_field',
	)

Now you can add ``GeopositionField`` to your model:

.. code:: python

	# models.py
	from django_geoposition_field.fields import GeopositionField

	class Model(models.Model):
		position = GeopositionField()


.. image:: https://raw.github.com/wiki/mireq/django-geoposition-field/admin.png?v2022-12-24


.. |codecov| image:: https://codecov.io/gh/mireq/django-geoposition-field/branch/master/graph/badge.svg?token=T801PBRI31
	:target: https://codecov.io/gh/mireq/django-geoposition-field

.. |version| image:: https://badge.fury.io/py/django-easy-geoposition-field.svg
	:target: https://pypi.python.org/pypi/django-easy-geoposition-field/

.. |downloads| image:: https://img.shields.io/pypi/dw/django-easy-geoposition-field.svg
	:target: https://pypi.python.org/pypi/django-easy-geoposition-field/

.. |license| image:: https://img.shields.io/pypi/l/django-easy-geoposition-field.svg
	:target: https://pypi.python.org/pypi/django-easy-geoposition-field/
