# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


DEFAULT_LENGTH = 100


class GeopositionField(models.Field):
	description = _("A geoposition (latitude and longitude)")

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('max_length', DEFAULT_LENGTH)
		super().__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'CharField'

	def from_db_value(self, value, *args, **kwargs):
		if not value:
			return None

		try:
			latitude, longitude = value.split(",")
			return Geoposition(latitude, longitude)
		except Exception: #pylint: disable=broad-except
			return None

	def get_prep_value(self, value):
		if not value:
			return ''
		else:
			return str(value)

	def formfield(self, **kwargs):
		defaults = {
			'form_class': GeopositionFormField
		}
		defaults.update(kwargs)
		return super().formfield(**defaults)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		if kwargs.get("max_length") == DEFAULT_LENGTH:
			del kwargs['max_length']
		return name, path, args, kwargs

	def to_python(self, value):
		if not value:
			return None
		latitude, longitude = value.split(",")
		return Geoposition(latitude, longitude)

	def value_to_string(self, obj):
		value = self.value_from_object(obj)
		return self.get_prep_value(value)
