===============================================
Django simple geoposition field with OSM widget
===============================================

Install
-------

`pip install https://github.com/mireq/django-geoposition_field.git`

Usage
-----

.. code:: python

	# settings.py
	INSTALLED_APPS = (
		# ...
		'django_geoposition_field',
	)

	# models.py
	from django_geoposition_field.fields import GeopositionField

	class Model(models.Model):
		position = GeopositionField()
