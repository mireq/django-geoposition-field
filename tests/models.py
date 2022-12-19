# -*- coding: utf-8 -*-
from django.db import models

from django_geoposition_field.fields import GeopositionField


class Address(models.Model):
	location = GeopositionField(blank=True, null=True)
	location2 = GeopositionField(blank=True, null=True, max_length=42) # just to check deconstruct

	def __str__(self):
		return f'{self.location} - {self.location2}'
