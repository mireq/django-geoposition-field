# -*- coding: utf-8 -*-
from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


class GeopositionField(models.Field):
	description = _("A geoposition (latitude and longitude)")
	default_error_messages = {
		'invalid': _("Enter a valid geoposition.")
	}

	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 100
		super().__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'CharField'

	def from_db_value(self, value, *args, **kwargs):
		if not value:
			return None
		if isinstance(value, Geoposition):
			return value
		if isinstance(value, list):
			return Geoposition(value[0], value[1])

		try:
			latitude, longitude = value.split(",")
			return Geoposition(latitude, longitude)
		except Exception: #pylint: disable=broad-except
			raise ValidationError(self.error_messages['invalid'], code='invalid')

	def get_prep_value(self, value):
		if not value:
			return ''
		elif isinstance(value, list):
			return ','.join(str(v) for v in value)
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
		if kwargs.get("max_length") == 100:
			del kwargs['max_length']
		return name, path, args, kwargs
